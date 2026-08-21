CREATE TABLE Dim_Date (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    full_date DATE UNIQUE,
    day_of_week VARCHAR(10),
    day_of_month INT,
    month INT,
    is_weekend BOOLEAN
);
 
CREATE TABLE Dim_Carrier (
    carrier_id INT AUTO_INCREMENT PRIMARY KEY,
    carrier_code VARCHAR(5) UNIQUE
);
 
CREATE TABLE Dim_Airport (
    airport_id INT AUTO_INCREMENT PRIMARY KEY,
    airport_code VARCHAR(5) UNIQUE,
    city_name VARCHAR(100)
);
 
CREATE TABLE Fact_Flights (
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    date_id INT,
    carrier_id INT,
    origin_airport_id INT,
    dest_airport_id INT,
    dep_delay DECIMAL(6,2),
    arr_delay DECIMAL(6,2),
    cancelled BOOLEAN,
    diverted BOOLEAN,
    carrier_delay DECIMAL(6,2),
    weather_delay DECIMAL(6,2),
    nas_delay DECIMAL(6,2),
    security_delay DECIMAL(6,2),
    late_aircraft_delay DECIMAL(6,2),
    FOREIGN KEY (date_id) REFERENCES Dim_Date(date_id),
    FOREIGN KEY (carrier_id) REFERENCES Dim_Carrier(carrier_id),
    FOREIGN KEY (origin_airport_id) REFERENCES Dim_Airport(airport_id),
    FOREIGN KEY (dest_airport_id) REFERENCES Dim_Airport(airport_id)
);