# Galactic-Cargo-Management-System
                                        Galactic Cargo Management System
                                            COL106 Assignment, 2024
A. Background
In the vast expanse of the galaxy, interstellar shipping companies face a critical challenge: efficiently packing cargo into their space cargo bins. Each cargo bin on a starship has a specific capacity, and each shipment of cargo comes in varying sizes and colors. Efficiently managing this cargo is essential for smooth space operations and avoiding costly delays. A new and upcoming company called The Galactic Cargo Management System (GCMS) needs your help to tackle this challenge.
The GCMS assigns unique integer IDs to both bins and objects. It handles cargo differ- ently based on the color of the cargo, which represents special handling instructions:

1. Blue Cargo (Compact Fit, Least ID): represents standard shipments, the system uses the Compact Fit Algorithm. This algorithm assigns the cargo to the bin with the smallest remaining capacity that is still sufficient to hold the item. If there are multiple bins with this remaining capacity, the one with the least ID is chosen.
2. Yellow Cargo (Compact Fit, Greatest ID): The Compact Fit algorithm is used for this color as well with the caveat that the bin with the greatest ID is chosen in case of multiple bins with the same remaining capacity.
3. Red Cargo (Largest Fit, Least ID): represents delicate items, the system uses the Largest Fit Algorithm. This algorithm assigns the cargo to the bin with the largest remaining capacity. If there are multiple bins with this remaining capacity, the one with the least ID is chosen.
4. Green Cargo (Largest Fit, Greatest ID): The Largest Fit algorithm is used for this color as well with the caveat that the bin with the greatest ID is chosen in case of multiple bins with the same remaining capacity.
B. Modelling
The problem in our context can be described as follows: there are n bins where each bin has a capacity and an ID which are both integers. We are also given objects in order where each object has a size and a ID which are again integers along with a color as mentioned above.
2.1 Largest Fit Algorithm:
The Largest Fit Algorithm is a well-known approach for solving the bin packing problem. When adding an object to a bin, this algorithm selects the bin with the largest remaining capacity.
2.2 Compact Fit Algorithm
The Compact Fit Algorithm is another algorithm for the bin packing problem. When adding an object to a bin, this algorithm selects the bin with the smallest remaining capacity that can accommodate this particular object.
3 Requirements
The GCMS will provide a unique identifier (ID) for each object and each cargo bin which can be any arbitrary integer. Note that two bins or two objects can have the same size.
Here’s a description of the classes and functionalities you are expected to implement:
3.1 GCMS
The constructor of this class initializes an empty system of cargo bins and objects. You need to implement the GCMS class with the below functions :
• add_bin(bin_id, capacity): Add a new bin with a specified ID and capacity.
• add_object(object_id, size, color): Add a new object with a specified ID, size and color choosing the appropriate algorithm based on the color of the object. Example :- (12345, 50, Color.RED)
Note : The bin capacity is reduced by the size of the added object in this operation.
• delete_object(object_id): Delete the object with the specified ID from its assigned bin.
• object_info(object_id): Print the ID of the bin the object has been placed into.
• bin_info(bin_id): Return a tuple with first element as the remaining capacity of the bin and second element as list of object IDs currently stored in the bin.
Example :- (44, [1432, 1340, 1500])