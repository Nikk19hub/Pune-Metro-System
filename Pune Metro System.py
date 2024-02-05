import heapq
import tkinter as tk
from tkinter import ttk


class Graph_M:
    class Vertex:
        def __init__(self):
            self.nbrs = {}

    def __init__(self):
        self.vtces = {}

    def num_vertex(self):
        return len(self.vtces)

    def contains_vertex(self, vname):
        return vname in self.vtces

    def add_vertex(self, vname):
        self.vtces[vname] = self.Vertex()

    def remove_vertex(self, vname):
        vtx = self.vtces[vname]
        keys = list(vtx.nbrs.keys())

        for key in keys:
            nbr_vtx = self.vtces[key]
            nbr_vtx.nbrs.pop(vname, None)

        self.vtces.pop(vname, None)

    def num_edges(self):
        count = 0
        for key, vtx in self.vtces.items():
            count += len(vtx.nbrs)
        return count // 2

    def contains_edge(self, vname1, vname2):
        vtx1 = self.vtces.get(vname1)
        vtx2 = self.vtces.get(vname2)
        return vtx1 and vtx2 and vname2 in vtx1.nbrs

    def add_edge(self, vname1, vname2, value):
        vtx1 = self.vtces.get(vname1)
        vtx2 = self.vtces.get(vname2)

        if vtx1 and vtx2 and vname2 not in vtx1.nbrs:
            vtx1.nbrs[vname2] = value
            vtx2.nbrs[vname1] = value

    def remove_edge(self, vname1, vname2):
        vtx1 = self.vtces.get(vname1)
        vtx2 = self.vtces.get(vname2)

        if vtx1 and vtx2 and vname2 in vtx1.nbrs:
            vtx1.nbrs.pop(vname2)
            vtx2.nbrs.pop(vname1)

    def display_map(self):
        print("\t Pune Metro Map")
        print("\t------------------")
        for key, vtx in self.vtces.items():
            print(key + " =>")
            for nbr, value in vtx.nbrs.items():
                print("\t" + nbr + "\t" + str(value))
        print("\t------------------")

    def display_stations(self):
        print("\n***********************************************************************\n")
        for i, key in enumerate(self.vtces, start=1):
            print(f"{i}. {key}")
        print("\n***********************************************************************\n")

    def dijkstra(self, start, end, weighted=True):
        if not self.contains_vertex(start) or not self.contains_vertex(end):
            return "INVALID STATIONS"

        distances = {vertex: float('infinity') for vertex in self.vtces}
        distances[start] = 0

        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_distance > distances[current_vertex]:
                continue

            for neighbor, weight in self.vtces[current_vertex].nbrs.items():
                distance = current_distance + (weight if weighted else 1)

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances[end]


# ... (the rest of your code remains unchanged)

class MetroApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Metro App")

        self.g = Graph_M()
        create_metro_map(self.g)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.master, text="WELCOME TO THE METRO APP", font=("Helvetica", 16)).pack(pady=10)

        self.actions_frame = ttk.Frame(self.master)
        self.actions_frame.pack(pady=10)

        ttk.Label(self.actions_frame, text="LIST OF ACTIONS", font=("Helvetica", 12)).grid(row=0, column=0,
                                                                                           columnspan=2)

        ttk.Button(self.actions_frame, text="List All Stations", command=self.list_stations).grid(row=1, column=0,
                                                                                                  pady=5)
        ttk.Button(self.actions_frame, text="Show Metro Map", command=self.show_map).grid(row=1, column=1, pady=5)
        ttk.Button(self.actions_frame, text="Get Shortest Distance", command=self.get_shortest_distance).grid(row=2,
                                                                                                              column=0,
                                                                                                              columnspan=2,
                                                                                                              pady=5)

    def list_stations(self):
        stations_window = tk.Toplevel(self.master)
        stations_window.title("List of Stations")

        ttk.Label(stations_window, text="List of Stations", font=("Helvetica", 12)).pack(pady=10)

        for i, key in enumerate(self.g.vtces, start=1):
            ttk.Label(stations_window, text=f"{i}. {key}").pack()

    def show_map(self):
        map_window = tk.Toplevel(self.master)
        map_window.title("Metro Map")

        ttk.Label(map_window, text="Pune Metro Map", font=("Helvetica", 12)).pack(pady=10)

        for key, vtx in self.g.vtces.items():
            ttk.Label(map_window, text=f"{key} =>").pack()
            for nbr, value in vtx.nbrs.items():
                ttk.Label(map_window, text=f"\t{nbr}\t{str(value)}").pack()

    def get_shortest_distance(self):
        distance_window = tk.Toplevel(self.master)
        distance_window.title("Shortest Distance")

        ttk.Label(distance_window, text="Enter Source Station:").pack()
        src_entry = ttk.Entry(distance_window)
        src_entry.pack()

        ttk.Label(distance_window, text="Enter Destination Station:").pack()
        dest_entry = ttk.Entry(distance_window)
        dest_entry.pack()

        ttk.Button(distance_window, text="Get Distance",
                   command=lambda: self.display_distance(src_entry.get(), dest_entry.get())).pack()

    def display_distance(self, src, dest):
        if not (self.g.contains_vertex(src) and self.g.contains_vertex(dest)):
            result_label = ttk.Label(self.master, text="INVALID INPUTS", font=("Helvetica", 12), foreground="red")
            result_label.pack(pady=10)
        else:
            distance = self.g.dijkstra(src, dest, False)
            result_label = ttk.Label(self.master, text=f"SHORTEST DISTANCE FROM {src} TO {dest} IS {distance} KM",
                                     font=("Helvetica", 12), foreground="green")
            result_label.pack(pady=10)


# Sample usage of the Graph_M class
def create_metro_map(g):
    g.add_vertex("PCMC")
    g.add_vertex("Sant Tukaram Nagar")
    g.add_vertex("Bhosari")
    g.add_vertex("Kasarwadi")
    g.add_vertex("Phugewadi")
    g.add_vertex("Dapodi")
    g.add_vertex("Bopodi")
    g.add_vertex("Shivaji Nagar")
    g.add_vertex("Civil Court")
    g.add_vertex("Budhwar Peth")
    g.add_vertex("Mandai")
    g.add_vertex("Swargate")
    g.add_vertex("Hill View Park Car Depot")
    g.add_vertex("Vanaz")
    g.add_vertex("Anand Nagar")
    g.add_vertex("Garware College")
    g.add_vertex("Deccan Gymkhana")
    g.add_vertex("Nal Stop")
    g.add_vertex("Chhatrapati Sambhaji Udyan")
    g.add_vertex("PMC")
    g.add_vertex("Mangalwar Peth")
    g.add_vertex("Pune Railway Station")
    g.add_vertex("Ruby Hall Clinic")
    g.add_vertex("Yerawada")
    g.add_vertex("Bund Garden")
    g.add_vertex("Kalyani Nagar")
    g.add_vertex("Ramwadi")

    g.add_edge("PCMC", "Sant Tukaram Nagar", 2)
    g.add_edge("Sant Tukaram Nagar", "Bhosari", 1)
    g.add_edge("Bhosari", "Kasarwadi", 2)
    g.add_edge("Kasarwadi", "Phugewadi", 1)
    g.add_edge("Phugewadi", "Dapodi", 1)
    g.add_edge("Dapodi", "Bopodi", 2)
    g.add_edge("Bopodi", "Shivaji Nagar", 5)
    g.add_edge("Shivaji Nagar", "Civil Court", 1)
    g.add_edge("Civil Court", "Budhwar Peth", 1)
    g.add_edge("Budhwar Peth", "Mandai", 1)
    g.add_edge("Mandai", "Swargate", 1)
    g.add_edge("Hill View Park Car Depot", "Vanaz", 1)
    g.add_edge("Vanaz", "Anand Nagar", 1)
    g.add_edge("Anand Nagar", "Nal Stop", 1)
    g.add_edge("Nal Stop", "Garware College", 1)
    g.add_edge("Garware College", "Deccan Gymkhana", 1)
    g.add_edge("Deccan Gymkhana", "Chhatrapati Sambhaji Udyan", 1)
    g.add_edge("Chhatrapati Sambhaji Udyan", "PMC", 1)
    g.add_edge("PMC", "Civil Court", 1)
    g.add_edge("Civil Court", "Mangalwar Peth", 1)
    g.add_edge("Mangalwar Peth", "Pune Railway Station", 1)
    g.add_edge("Pune Railway Station", "Ruby Hall Clinic", 1)
    g.add_edge("Ruby Hall Clinic", "Yerwada", 2)
    g.add_edge("Yerwada", "Bund Garden", 3)
    g.add_edge("Bund Garden", "Kalyani Nagar", 2)
    g.add_edge("Kalyani Nagar", "Ramwadi", 3)


if __name__ == "__main__":
    g = Graph_M()
    create_metro_map(g)
    root = tk.Tk()
    app = MetroApp(root)
    root.mainloop()
    print("\n\t\t\t****WELCOME TO THE METRO APP*****")

    while True:
        print("\t\t\t\t~~LIST OF ACTIONS~~\n\n")
        print("1. LIST ALL THE STATIONS IN THE MAP")
        print("2. SHOW THE METRO MAP")
        print("3. GET SHORTEST DISTANCE FROM A 'SOURCE' STATION TO 'DESTINATION' STATION")
        print("4. EXIT THE MENU")
        print("\nENTER YOUR CHOICE FROM THE ABOVE LIST (1 to 4) : ")

        choice = int(input())

        if choice == 4:
            break

        if choice == 1:
            g.display_stations()
        elif choice == 2:
            g.display_map()
        elif choice == 3:
            print("ENTER THE SOURCE AND DESTINATION STATIONS")
            src = input()
            dest = input()

            if not (g.contains_vertex(src) and g.contains_vertex(dest)):
                print("INVALID INPUTS")
            else:
                print(f"SHORTEST DISTANCE FROM {src} TO {dest} IS {g.dijkstra(src, dest, False)} KM")
        else:
            print("Please enter a valid option! ")