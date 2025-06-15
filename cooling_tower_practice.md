# Cooling Tower Best Practices

## Water Conductivity

Conductivity is a measure of the water's ability to conduct electricity and is an indicator of the total dissolved solids (TDS) in the water. In cooling towers, managing conductivity is crucial for preventing scale, corrosion, and biological growth.

### Bleed-off Conductivity

The bleed-off (or blowdown) conductivity is a key operational parameter. The sensor `ChPlt.bleed_off_conductivity` measures this value.

- **Optimal Range**: The typical control range for conductivity in an open-loop cooling tower is between **1,500 and 2,500 microsiemens/cm (µS/cm)**.
- **High Conductivity (> 2,500 µS/cm)**: If the conductivity is too high, it indicates an excessive concentration of dissolved solids. This can lead to the formation of mineral scale on heat exchange surfaces, which insulates the surfaces and reduces heat transfer efficiency. This forces the chiller to work harder, consuming more energy. It can also accelerate corrosion.
- **Low Conductivity (< 1,500 µS/cm)**: If the conductivity is too low, it may indicate excessive bleed-off, which means too much water is being drained and replaced. This is wasteful in terms of both water and the chemicals used for water treatment.

## Thermal Comfort

Thermal comfort in a room is affected by several factors:

- **Temperature**: Generally, a temperature between 20°C and 24°C is considered comfortable.
- **Humidity**: Relative humidity between 40% and 60% is ideal. High humidity can make a room feel stuffy and warm, while low humidity can cause dry skin and static electricity.
- **Air Movement**: Gentle air circulation helps maintain an even temperature and can improve comfort.

If a user feels cold, it could be due to the temperature being at the lower end of the spectrum or even slightly below it. It is important to check the sensor readings and adjust the setpoint if necessary. 

## Airflow Rate

Airflow rate, typically measured in meters per second (m/s), is the speed at which air moves through a space or system (like a cooling tower).

- **Importance in Cooling Towers**: In the context of a cooling tower, a higher airflow rate generally leads to more efficient cooling because it increases the rate of evaporation. However, this comes at the cost of higher energy consumption by the fan. The system is balanced to provide effective cooling without excessive energy use.
- **Importance for Thermal Comfort**: In an office environment, airflow (or air movement) is a key factor in thermal comfort. Gentle air circulation can help maintain an even temperature and prevent feelings of stuffiness. However, excessive airflow can feel like a draft and cause occupants to feel cold, even if the temperature is within a normal range. 