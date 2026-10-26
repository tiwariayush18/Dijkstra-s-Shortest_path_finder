import tkinter as tk
from tkinter import ttk, messagebox

# Locations and their positions
places = {
    "A": (70, 65),
    "B": (210, 65),
    "C": (350, 65),
    "D": (490, 65),
    "E": (630, 65),
    "F": (70, 170),
    "G": (210, 170),
    "H": (350, 170),
    "I": (490, 170),
    "J": (630, 170),
    "K": (210, 275),
    "L": (420, 275),
    "M": (630, 275)
}

# Roads and their distances
graph = {
    "A": {"B": 4, "F": 7, "G": 9},
    "B": {"A": 4, "C": 6, "G": 3, "H": 8},
    "C": {"B": 6, "D": 5, "G": 4, "H": 2, "I": 7},
    "D": {"C": 5, "E": 3, "H": 6, "I": 4, "J": 8},
    "E": {"D": 3, "I": 9, "J": 5},
    "F": {"A": 7, "G": 2, "H": 10, "K": 6},
    "G": {"A": 9, "B": 3, "C": 4, "F": 2, "H": 3, "K": 5, "L": 8},
    "H": {"B": 8, "C": 2, "D": 6, "F": 10, "G": 3, "I": 2, "K": 7, "L": 4, "M": 11},
    "I": {"C": 7, "D": 4, "E": 9, "H": 2, "J": 3, "L": 5, "M": 9},
    "J": {"D": 8, "E": 5, "I": 3, "L": 7, "M": 4},
    "K": {"F": 6, "G": 5, "H": 7, "L": 3},
    "L": {"G": 8, "H": 4, "I": 5, "J": 7, "K": 3, "M": 2},
    "M": {"H": 11, "I": 9, "J": 4, "L": 2}
}

def dijkstra(start, end):
    distance = {place: float("inf") for place in graph}
    previous = {}
    unvisited = list(graph)

    distance[start] = 0

    while unvisited:
        current = min(unvisited, key=lambda x: distance[x])
        unvisited.remove(current)

        if distance[current] == float("inf"):
            break

        if current == end:
            break

        for neighbour, cost in graph[current].items():
            new_distance = distance[current] + cost

            if new_distance < distance[neighbour]:
                distance[neighbour] = new_distance
                previous[neighbour] = current

    if distance[end] == float("inf"):
        return [], 0

    path = []
    current = end

    while current != start:
        path.append(current)
        current = previous[current]

    path.append(start)
    path.reverse()

    return path, distance[end]


def draw_graph(path=None):
    canvas.delete("all")
    path = path or []

    # Draw roads
    for place in graph:
        for neighbour, cost in graph[place].items():
            if places[place] < places[neighbour]:
                x1, y1 = places[place]
                x2, y2 = places[neighbour]

                color = "#22c55e" if (
                    place in path and neighbour in path
                    and abs(path.index(place) - path.index(neighbour)) == 1
                ) else "#64748b"

                canvas.create_line(
                    x1, y1, x2, y2,
                    fill=color, width=5 if color == "#22c55e" else 2
                )

                canvas.create_text(
                    (x1 + x2) / 2, (y1 + y2) / 2 - 12,
                    text=str(cost), fill="white", font=("Arial", 11)
                )

    # Draw locations
    for place, (x, y) in places.items():
        color = "#22c55e" if place in path else "#2563eb"

        canvas.create_oval(
            x - 22, y - 22, x + 22, y + 22,
            fill=color, outline="white", width=2
        )
        canvas.create_text(
            x, y, text=place, fill="white",
            font=("Arial", 14, "bold")
        )


def find_path():
    start = start_box.get()
    end = end_box.get()

    if start == end:
        messagebox.showinfo("Result", "Start aur destination same hain.")
        draw_graph([start])
        result_label.config(text="Total Distance: 0")
        return

    path, total = dijkstra(start, end)
    draw_graph(path)

    if path:
        result_label.config(
            text="Path: " + " -> ".join(path)
            + "\nTotal Distance: " + str(total)
        )
    else:
        result_label.config(text="Koi path nahi mila.")


# Main window
root = tk.Tk()
root.title("Dijkstra Shortest Path Finder")
root.geometry("900x720")
root.configure(bg="#0f172a")

title = tk.Label(
    root, text="DIJKSTRA SHORTEST PATH FINDER",
    font=("Arial", 18, "bold"),
    bg="#0f172a", fg="#38bdf8"
)
title.pack(pady=12)

controls = tk.Frame(root, bg="#0f172a")
controls.pack(pady=5)

tk.Label(
    controls, text="Start:", bg="#0f172a", fg="white"
).grid(row=0, column=0, padx=5)

start_box = ttk.Combobox(
    controls, values=list(graph.keys()),
    state="readonly", width=5
)
start_box.set("A")
start_box.grid(row=0, column=1, padx=5)

tk.Label(
    controls, text="Destination:", bg="#0f172a", fg="white"
).grid(row=0, column=2, padx=5)

end_box = ttk.Combobox(
    controls, values=list(graph.keys()),
    state="readonly", width=5
)
end_box.set("M")
end_box.grid(row=0, column=3, padx=5)

button = tk.Button(
    controls, text="Find Shortest Path",
    command=find_path, bg="#22c55e",
    fg="black", font=("Arial", 10, "bold")
)
button.grid(row=0, column=4, padx=10)

canvas = tk.Canvas(
    root, width=720, height=340,
    bg="#1e293b", highlightthickness=0
)
canvas.pack(pady=10)

result_label = tk.Label(
    root, text="Select locations and find the shortest path",
    font=("Arial", 12, "bold"),
    bg="#0f172a", fg="#facc15"
)
result_label.pack(pady=5)

draw_graph()
find_path()
root.mainloop()
