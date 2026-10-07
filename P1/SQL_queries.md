1) Which hours of the day are the most expensive per season?

~~~~sql
WITH HourlySeasonPrice AS (
    SELECT
        d.Season,
        t.Hour,
        AVG(e.Price) AS AvgPrice
    FROM FactEnergyHourly e
    JOIN DimDate d
        ON e.DateKey = d.DateKey
    JOIN DimTime t
        ON e.TimeKey = t.TimeKey
    WHERE e.Price IS NOT NULL
    GROUP BY
        d.Season,
        t.Hour
),
RankedHours AS (
    SELECT
        Season,
        Hour,
        AvgPrice,
        RANK() OVER (
            PARTITION BY Season
            ORDER BY AvgPrice DESC
        ) AS PriceRank
    FROM HourlySeasonPrice
)
SELECT
    Season,
    Hour,
    ROUND(AvgPrice, 2) AS AvgPrice
FROM RankedHours
WHERE PriceRank <= 3
ORDER BY
    Season,
    PriceRank;
~~~~

2) How is temperature related to electricity consumption?

~~~~sql
WITH HourlyWeather AS (
    SELECT
        DateKey,
        TimeKey,
        AVG(AirTemperature) AS AirTemperature
    FROM FactWeatherHourly
    WHERE AirTemperature IS NOT NULL
    GROUP BY
        DateKey,
        TimeKey
),
Bucketed AS (
    SELECT
        e.Consumption,
        w.AirTemperature,
        CASE
            WHEN w.AirTemperature < -20 THEN '< -20'
            WHEN w.AirTemperature < -10 THEN '[-20, -10)'
            WHEN w.AirTemperature <   0 THEN '[-10, 0)'
            WHEN w.AirTemperature <  10 THEN '[0, 10)'
            WHEN w.AirTemperature <  20 THEN '[10, 20)'
            WHEN w.AirTemperature <  30 THEN '[20, 30)'
            ELSE '30+'
        END AS TemperatureRange
    FROM FactEnergyHourly e
    JOIN HourlyWeather w
        ON  w.DateKey = e.DateKey
        AND w.TimeKey = e.TimeKey
    WHERE e.Consumption IS NOT NULL
)
SELECT
    TemperatureRange,
    ROUND(AVG(Consumption), 1) AS AvgConsumption,
    COUNT(*)                   AS Hours
FROM Bucketed
GROUP BY TemperatureRange
ORDER BY MIN(AirTemperature);
~~~~

3) How does the average electricity price differ between high-wind hours and calm wind hours?

~~~~sql
WITH HourlyWeather AS (
    SELECT
        DateKey,
        TimeKey,
        AVG(WindSpeed) AS WindSpeed
    FROM FactWeatherHourly
    WHERE WindSpeed IS NOT NULL
    GROUP BY
        DateKey,
        TimeKey
),
HourlyData AS (
    SELECT
        e.Price,
        w.WindSpeed
    FROM FactEnergyHourly e
    JOIN HourlyWeather w
        ON  w.DateKey = e.DateKey
        AND w.TimeKey = e.TimeKey
    WHERE e.Price IS NOT NULL
),
WindThresholds AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY WindSpeed) AS CalmThreshold,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY WindSpeed) AS HighWindThreshold
    FROM HourlyData
),
Classified AS (
    SELECT
        h.Price,
        CASE
            WHEN h.WindSpeed <= t.CalmThreshold     THEN 'Calm wind'
            WHEN h.WindSpeed >= t.HighWindThreshold THEN 'High wind'
            ELSE 'Medium wind'
        END AS WindCategory
    FROM HourlyData h
    CROSS JOIN WindThresholds t
)
SELECT
    WindCategory,
    ROUND(AVG(Price), 2) AS AvgPrice,
    COUNT(*)             AS Hours
FROM Classified
GROUP BY WindCategory
ORDER BY AvgPrice;
~~~~

4) On which days were prices near zero (or negative) and what were the weather conditions then?

~~~~sql
WITH HourlyWeather AS (
    SELECT
        DateKey,
        TimeKey,
        AVG(AirTemperature)  AS AvgAirTemperature,
        AVG(WindSpeed)       AS AvgWindSpeed,
        MAX(WindSpeedMax)    AS MaxWindSpeed,
        AVG(Precipitations)  AS AvgPrecipitations
    FROM FactWeatherHourly
    GROUP BY
        DateKey,
        TimeKey
)
SELECT
    d.DateFull,
    t.Hour,
    e.Price,
    ROUND(w.AvgAirTemperature, 1) AS AvgAirTemperature,
    ROUND(w.AvgWindSpeed, 1)      AS AvgWindSpeed,
    w.MaxWindSpeed,
    ROUND(w.AvgPrecipitations, 1) AS AvgPrecipitations,
    e.WindProduction,
    e.SolarProduction,
    e.RenewableShare,
    e.Production,
    e.Consumption
FROM FactEnergyHourly e
JOIN DimDate d
    ON e.DateKey = d.DateKey
JOIN DimTime t
    ON e.TimeKey = t.TimeKey
LEFT JOIN HourlyWeather w
    ON  w.DateKey = e.DateKey
    AND w.TimeKey = e.TimeKey
WHERE e.Price <= 5  -- low-price threshold in EUR/MWh, can be changed
ORDER BY
    d.DateFull,
    t.Hour;
~~~~

5) What features correlate the best with near-zero (or negative) energy prices?

~~~~sql
WITH HourlyWeather AS (
    SELECT
        DateKey,
        TimeKey,
        AVG(AirTemperature)   AS AirTemperature,
        AVG(WindSpeed)        AS WindSpeed,
        MAX(WindSpeedMax)     AS WindSpeedMax,
        AVG(Precipitations)   AS Precipitations,
        AVG(SunshineDuration) AS SunshineDuration
    FROM FactWeatherHourly
    GROUP BY
        DateKey,
        TimeKey
),
PriceClassification AS (
    SELECT
        CASE WHEN e.Price <= 5 THEN 1.0 ELSE 0.0 END AS NearZeroPrice,  -- threshold can be changed
        w.AirTemperature,
        w.WindSpeed,
        w.WindSpeedMax,
        w.Precipitations,
        w.SunshineDuration,
        e.WindProduction,
        e.SolarProduction,
        e.RenewableShare,
        e.Production,
        e.Consumption
    FROM FactEnergyHourly e
    LEFT JOIN HourlyWeather w
        ON  w.DateKey = e.DateKey
        AND w.TimeKey = e.TimeKey
    WHERE e.Price IS NOT NULL
)
SELECT
    Feature,
    ROUND(Correlation::numeric, 3) AS Correlation
FROM (
    SELECT 'AirTemperature'   AS Feature, CORR(NearZeroPrice, AirTemperature)   AS Correlation FROM PriceClassification
    UNION ALL
    SELECT 'WindSpeed',        CORR(NearZeroPrice, WindSpeed)        FROM PriceClassification
    UNION ALL
    SELECT 'WindSpeedMax',     CORR(NearZeroPrice, WindSpeedMax)     FROM PriceClassification
    UNION ALL
    SELECT 'Precipitations',   CORR(NearZeroPrice, Precipitations)   FROM PriceClassification
    UNION ALL
    SELECT 'SunshineDuration', CORR(NearZeroPrice, SunshineDuration) FROM PriceClassification
    UNION ALL
    SELECT 'WindProduction',   CORR(NearZeroPrice, WindProduction)   FROM PriceClassification
    UNION ALL
    SELECT 'SolarProduction',  CORR(NearZeroPrice, SolarProduction)  FROM PriceClassification
    UNION ALL
    SELECT 'RenewableShare',   CORR(NearZeroPrice, RenewableShare)   FROM PriceClassification
    UNION ALL
    SELECT 'Production',       CORR(NearZeroPrice, Production)       FROM PriceClassification
    UNION ALL
    SELECT 'Consumption',      CORR(NearZeroPrice, Consumption)      FROM PriceClassification
) c
ORDER BY ABS(Correlation) DESC NULLS LAST;
~~~~
