# Supermarket Case Study

This is a simple simulation that arised from a conversation I had with a Supermarket owner.

The supermarket chain had over a 194 stores scattered across the city of Belo Horizonte, MG - Brazil and around 20,000 employees.

According to Brazilian law, they are required to provide their emplyees with the money to commute to and from work to their houses, and therefore spent a lot of money with this.

The idea here was to simulate their business operations in a smaller scale, however the idea remains the same. Reduce the total combined distance travelled of all employees.

The file employee_store_generation.py generates 200 fictional stores and 20,000 fictional employees that will later be allocated within the stores. This file returns two .csv files that will later be used by the code employee_store_generator.py

Finally the code employee_allocation.py will iterate through 10,000 different allocation possibilities and return the best result.

The best result is defined by the lowest possible sum of distances between the stores and allocated employees.
