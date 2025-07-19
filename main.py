import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY", "your-api-key-here"))
print(client)
# Part 1: Calculate elevator requirements with OpenAI integration
def calculate_elevator_requirements():
    """Calculate elevator requirements using OpenAI and return (capacity, number of people, number of lifts)."""
    # Collect inputs as plain strings
    F = input("Enter the number of floors: ")
    M = input("Enter the maximum building capacity in people: ")
    Q = input("Enter the peak number of people per 5 minutes: ")
    t = input("Enter the average time to travel between two floors in seconds: ")
    desired_waiting_time = input("Enter the desired maximum waiting time in seconds: ")

    # Prepare input for OpenAI
    prompt = f"""
    A building has the following elevator system parameters:
    - Number of floors: {F}
    - Maximum building capacity: {M} people
    - Peak number of people per 5 minutes: {Q}
    - Average time to travel between two floors: {t} seconds
    - Desired maximum waiting time: {desired_waiting_time} seconds

    As an elevator system design expert, please:
    1. Suggest a reasonable capacity per elevator (in people) based on the building parameters.
    2. Calculate the minimum number of lifts required to meet the waiting time and peak demand.
    3. Provide the result as a tuple: (capacity, number of people, number of lifts), where 'number of people' is typically the same as the capacity per lift.
    4. Validate the calculations and explain if the tuple is reasonable for the building's needs.
    5. If applicable, suggest adjustments or considerations, especially regarding the maximum building capacity.

    Your output must only be a single line, in this exact format, with no explanation, no reasoning, no additional text:

    Tuple: (capacity, number of people, number of lifts)
    where:

    capacity = recommended number of people per elevator (integer)

    number of people = peak number of people per 5 minutes (from input)

    number of lifts = calculated number of lifts required (integer)

    Do not include any formulas, steps, validation, or considerations.
    Respond with nothing but the tuple in the above format.
    """

    # Call OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an elevator system design expert. Provide concise, accurate, and practical responses. Output only in the following format: Tuple: (capacity, number of people, number of lifts)"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        openai_response = response.choices[0].message.content

        # Extract tuple from OpenAI response (assuming it follows the requested format)
        # This is a simple parsing approach; in production, you might use regex or structured output
        try:
            # Look for the tuple in the response, e.g., "Tuple: (20, 20, 2)"
            tuple_start = openai_response.find("Tuple: (")
            if tuple_start != -1:
                tuple_str = openai_response[tuple_start + 7:openai_response.find(")", tuple_start) + 1]
                # Parse the tuple string, e.g., "(20, 20, 2)"
                values = eval(tuple_str)  # Safe for simple integers in this context
                result = values
            else:
                result = (20, 20, 2)  # Fallback default if parsing fails
                openai_response += "\nWarning: Could not parse tuple from OpenAI response. Using default (20, 20, 2)."
        except Exception as e:
            result = (20, 20, 2)  # Fallback default
            openai_response += f"\nError parsing OpenAI response: {str(e)}. Using default (20, 20, 2)."
    except Exception as e:
        openai_response = f"Error calling OpenAI API: {str(e)}"
        result = (20, 20, 2)  # Fallback default

    # Output results
    print("\n=== Elevator Requirements Calculation ===")
    print(f"Output tuple (capacity, number of people, number of lifts): {result}")
    print("\n=== OpenAI Validation ===")
    print(openai_response)

    return result

# Part 2: Elevator scheduling
class Elevator:
    """Represents an elevator with its current state and behavior."""
    def __init__(self, id, capacity, floors):
        self.id = id
        self.capacity = capacity
        self.current_floor = 1
        self.direction = "idle"  # "up", "down", or "idle"
        self.load = 0
        self.destinations = []
        self.floors = floors

    def add_destination(self, floor):
        """Add a floor to the elevator's destination list and sort based on direction."""
        if floor not in self.destinations and 1 <= floor <= self.floors:
            self.destinations.append(floor)
            if self.direction == "up":
                self.destinations.sort()
            elif self.direction == "down":
                self.destinations.sort(reverse=True)

    def is_full(self, threshold=0.8):
        """Check if the elevator is near maximum capacity."""
        return self.load >= threshold * self.capacity

class Building:
    """Manages elevators and handles passenger requests."""
    def __init__(self, floors, num_lifts, capacity):
        self.floors = floors
        self.elevators = [Elevator(i, capacity, floors) for i in range(num_lifts)]
        self.requests = {}  # {floor: direction}

    def add_request(self, floor, direction):
        """Add a new request and assign an elevator."""
        if 1 <= floor <= self.floors and direction in ["up", "down"]:
            self.requests[floor] = direction
            assigned_elevator = self.assign_elevator(floor, direction)
            if assigned_elevator:
                assigned_elevator.add_destination(floor)
                print(f"Elevator {assigned_elevator.id} assigned to floor {floor} going {direction}")
            else:
                print(f"No suitable elevator available for floor {floor} going {direction}")

    def assign_elevator(self, floor, direction):
        """Assign the nearest suitable elevator based on guidelines."""
        candidates = []
        for elevator in self.elevators:
            if elevator.is_full():
                continue
            if elevator.direction == "idle":
                distance = abs(elevator.current_floor - floor)
                candidates.append((distance, elevator))
            elif elevator.direction == direction:
                if (direction == "up" and elevator.current_floor < floor) or \
                   (direction == "down" and elevator.current_floor > floor):
                    distance = abs(elevator.current_floor - floor)
                    candidates.append((distance, elevator))
        if candidates:
            candidates.sort(key=lambda x: x[0])
            return candidates[0][1]
        return None

# Example usage
if __name__ == "__main__":
    # Part 1: Determine elevator requirements with OpenAI
    print("=== Elevator Requirements Calculation with OpenAI ===")
    capacity, num_people, num_lifts = calculate_elevator_requirements()

    # Part 2: Simulate elevator scheduling
    print("\n=== Elevator Scheduling Simulation ===")
    building = Building(floors=10, num_lifts=num_lifts, capacity=capacity)
    # Example requests
    building.add_request(3, "up")
    building.add_request(5, "down")
    building.add_request(7, "up")