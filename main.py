import numpy as np
import matplotlib.pyplot as plt


# -----------------------------
# Problem configuration
# -----------------------------

NUM_CUSTOMERS = 3
NUM_VEHICLES = 2

np.random.seed(42)


# -----------------------------
# Generate locations
# -----------------------------

# Node 0 = depot
# Nodes 1...N = customers

locations = np.random.rand(
    NUM_CUSTOMERS + 1,
    2
) * 10

print("Locations:")
for i, location in enumerate(locations):

    if i == 0:
        print(f"Depot:     {location}")
    else:
        print(f"Customer {i}: {location}")
        
# -----------------------------
# Calculate distance matrix
# -----------------------------

distance_matrix = np.zeros(
    (NUM_CUSTOMERS + 1,
     NUM_CUSTOMERS + 1)
)

for i in range(NUM_CUSTOMERS + 1):

    for j in range(NUM_CUSTOMERS + 1):

        distance_matrix[i][j] = np.linalg.norm(
            locations[i] - locations[j]
        )


print("\nDistance Matrix:")
print(np.round(distance_matrix, 2))

# -----------------------------
# Visualize locations
# -----------------------------

plt.figure(figsize=(8, 6))

# Plot depot
plt.scatter(
    locations[0][0],
    locations[0][1],
    marker="*",
    s=250,
    label="Depot"
)

# Plot customers
plt.scatter(
    locations[1:, 0],
    locations[1:, 1],
    s=100,
    label="Customers"
)

# Add labels
for i, (x, y) in enumerate(locations):

    if i == 0:
        label = "Depot"
    else:
        label = f"C{i}"

    plt.annotate(
        label,
        (x, y),
        xytext=(5, 5),
        textcoords="offset points"
    )

plt.xlabel("X")
plt.ylabel("Y")
plt.title("VRP Problem Instance")
plt.legend()
plt.grid(True)

plt.show()