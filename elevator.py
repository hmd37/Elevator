import time
from queue import PriorityQueue


class Elevator:
    def __init__(self, total_floors):
        self.current_floor = 1
        self.direction = "idle"  
        self.requests = PriorityQueue()  
        self.total_floors = total_floors
        self.max_requests = 3  

    def add_request(self, floor):
        if floor == self.current_floor:
            print(f"Request for floor {floor} ignored (already on this floor).")
            return

        existing_requests = [f[1] for f in self.requests.queue]
        if floor in existing_requests:
            print(f"Request for floor {floor} ignored (already requested).")
            return

        if self.requests.qsize() < self.max_requests:
            if 1 <= floor <= self.total_floors:
                priority = abs(floor - self.current_floor)
                self.requests.put((priority, floor))
                print(f"Request for floor {floor} added.")
            else:
                print(f"Invalid floor {floor}.")

    def process_requests(self):
        while not self.requests.empty():
            _, target_floor = self.requests.get()

            if target_floor > self.current_floor:
                self.direction = "up"
            elif target_floor < self.current_floor:
                self.direction = "down"
            else:
                self.direction = "idle"

            while self.current_floor != target_floor:
                time.sleep(1)  # Simulate movement time

                if self.direction == "up":
                    self.current_floor += 1
                elif self.direction == "down":
                    self.current_floor -= 1

                self.display_elevator_status(target_floor)

                self._handle_intermediate_requests()

            print(f"Stopped at floor {self.current_floor}. Doors opening...")
            time.sleep(2)  # Simulate door open/close
            print("Doors closed.")

        self.direction = "idle"
        print(f"Elevator is idle at floor {self.current_floor}.")

    def display_elevator_status(self, target_floor):
        floors = range(self.total_floors, 0, -1)  # Top to bottom
        """Displays the elevator shaft and its status in the terminal."""
        print("\033c", end="")  # Clear the terminal for dynamic updates
        print(f"Elevator Status: Moving {self.direction}, Target: Floor {target_floor}")
        print(f"Current Floor: {self.current_floor}\n")

        for floor in floors:
            if floor == self.current_floor:
                print(f"Floor {floor:2} | [E]  <-- Elevator here")
            elif floor == target_floor:
                print(f"Floor {floor:2} | [T]  <-- Target floor")
            else:
                print(f"Floor {floor:2} |")
        print("-" * 20)

    def _handle_intermediate_requests(self):
        intermediate_requests = []
        while not self.requests.empty():
            _, intermediate_floor = self.requests.get()
            if intermediate_floor == self.current_floor:
                print(f"Stopping at floor {self.current_floor} for an intermediate request.")
                print("Doors opening...")
                time.sleep(2)  # Simulate door open/close
                print("Doors closed.")
            else:
                intermediate_requests.append((abs(intermediate_floor - self.current_floor), intermediate_floor))

        # Re-add remaining requests to the queue
        for request in intermediate_requests:
            self.requests.put(request)
