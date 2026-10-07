1) Which hours of the day are the most expensive per season?

~~~~sql
WITH HourlySeasonPrice AS (
    SELECT
        d.Season,
        t.Hour,
        AVG(f.Price) AS AvgPrice
    FROM FactWeatherEnergy f
    JOIN DimDate d
        ON f.DateKey = d.DateKey
    JOIN DimTime t
        ON f.TimeKey = t.TimeKey
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
    AvgPrice
FROM RankedHours
WHERE PriceRank <= 3
ORDER BY
    Season,
    PriceRank;
~~~~

2) How is temperature related to electricity consumption?

~~~~sql
SELECT
    CASE
        WHEN AirTemperature < -20 THEN '<-20°C'        
        WHEN AirTemperature < -10 THEN '-20—-11°C'
        WHEN AirTemperature < 0 THEN '-10–-1°C'
        WHEN AirTemperature < 10 THEN '0–9°C'
        WHEN AirTemperature < 20 THEN '10–19°C'
        WHEN AirTemperature < 30 THEN '20–29°C'
        ELSE '30+°C'
    END AS TemperatureRange,
    AVG(Consumption) AS AvgConsumption,
    COUNT(*) AS Observations
FROM FactWeatherEnergy
WHERE
    AirTemperature IS NOT NULL
    AND Consumption IS NOT NULL
GROUP BY
    CASE
        WHEN AirTemperature < -20 THEN '<-20°C'        
        WHEN AirTemperature < -10 THEN '-20—-11°C'
        WHEN AirTemperature < 0 THEN '-10–-1°C'
        WHEN AirTemperature < 10 THEN '0-9°C'
        WHEN AirTemperature < 20 THEN '10-19°C'
        WHEN AirTemperature < 30 THEN '20-29°C'
        ELSE '30+°C'
    END
ORDER BY
    MIN(AirTemperature);
~~~~

3) How does the average electricity price differ between high-wind hours and calm wind hours?

~~~~sql
WITH WindThresholds AS (
    SELECT
        PERCENTILE_CONT(0.25)
            WITHIN GROUP (ORDER BY WindSpeed) AS CalmThreshold,
        PERCENTILE_CONT(0.75)
            WITHIN GROUP (ORDER BY WindSpeed) AS HighWindThreshold
    FROM FactWeatherEnergy
    WHERE WindSpeed IS NOT NULL
),
Classified AS (
    SELECT
        f.Price,
        f.WindSpeed,
        CASE
            WHEN f.WindSpeed <= w.CalmThreshold
                THEN 'Calm wind'
            WHEN f.WindSpeed >= w.HighWindThreshold
                THEN 'High wind'
            ELSE 'Medium wind'
        END AS WindCategory
    FROM FactWeatherEnergy f
    CROSS JOIN WindThresholds w
    WHERE
        f.WindSpeed IS NOT NULL
        AND f.Price IS NOT NULL
)
SELECT
    WindCategory,
    AVG(Price) AS AvgPrice,
    COUNT(*) AS Observations
FROM Classified
GROUP BY WindCategory
ORDER BY AvgPrice;
~~~~

4) On which days were prices near zero (or negative) and what were the weather conditions then?

~~~~sql
SELECT
    d.DateFull,
    t.Hour,
    f.Price,
    f.AirTemperature,
    f.WindSpeed,
    f.WindSpeedMax,
    f.Precipitations,
    f.SunshineDuration,
    f.WindProduction,
    f.SolarProduction,
    f.Production,
    f.Consumption
FROM FactWeatherEnergy f
JOIN DimDate d
    ON f.DateKey = d.DateKey
JOIN DimTime t
    ON f.TimeKey = t.TimeKey
WHERE f.Price <= 5 -- This is low price threshold, it can be changed
ORDER BY
    d.DateFull,
    t.Hour;
~~~~

5) What features correlate the best with near-zero (or negative) energy prices?

~~~~sql
WITH PriceClassification AS (
    SELECT
        CASE
            WHEN Price <= 5 THEN 1.0  -- This is low price threshold, it can also be changed
            ELSE 0.0
        END AS NearZeroPrice,

        AirTemperature,
        WindSpeed,
        WindSpeedMax,
        Precipitations,
        SunshineDuration,
        WindProduction,
        SolarProduction,
        Production,
        Consumption
    FROM FactWeatherEnergy
)
SELECT
    'AirTemperature' AS Feature,
    CORR(NearZeroPrice, AirTemperature) AS Correlation
FROM PriceClassification

UNION ALL

SELECT
    'WindSpeed',
    CORR(NearZeroPrice, WindSpeed)
FROM PriceClassification

UNION ALL

SELECT
    'WindSpeedMax',
    CORR(NearZeroPrice, WindSpeedMax)
FROM PriceClassification

UNION ALL

SELECT
    'Precipitations',
    CORR(NearZeroPrice, Precipitations)
FROM PriceClassification

UNION ALL

SELECT
    'SunshineDuration',
    CORR(NearZeroPrice, SunshineDuration)
FROM PriceClassification

UNION ALL

SELECT
    'WindProduction',
    CORR(NearZeroPrice, WindProduction)
FROM PriceClassification

UNION ALL

SELECT
    'SolarProduction',
    CORR(NearZeroPrice, SolarProduction)
FROM PriceClassification

UNION ALL

SELECT
    'Production',
    CORR(NearZeroPrice, Production)
FROM PriceClassification

UNION ALL

SELECT
    'Consumption',
    CORR(NearZeroPrice, Consumption)
FROM PriceClassification

ORDER BY ABS(Correlation) DESC;
~~~~
