import json

def calculate_velocity_score(parent_data):
    def check_velocity_conditions(v, v_avg, tolerance=0.05):
        if v == 0:
            return False
            
        # Check if velocity is within a small percentage (5%) of the average velocity
        if abs(v - v_avg) < tolerance * v_avg:
            return True
            
        v_ratio = v / v_avg
        if v_ratio >= 2:
            k = 1
            # Check if the ratio is close to a power of 2 (within 5% tolerance of v_avg)
            while 2**k <= v_ratio + tolerance:
                if abs(v_ratio - 2**k) < tolerance:
                    return True
                k += 1
                
        # Check if velocity is close to an even multiple of 2 * v_avg
        if abs(v % (2 * v_avg)) < tolerance * (2 * v_avg):
            return True
            
        return False

    instruments = []
    total_velocity = 0
    valid_instruments = []
    
    for instrument in parent_data:
        if instrument:
            velocity_mean = instrument[0].get('velocity_mean', 0)
            category = instrument[0].get('instrument_category', 'Unknown')
            instruments.append({
                'velocity': velocity_mean,
                'category': category
            })
            total_velocity += velocity_mean
        else:
            instruments.append({
                'velocity': 0,
                'category': 'Empty'
            })

    num_instruments = len(instruments)
    v_avg = total_velocity / num_instruments if num_instruments > 0 else 0

    for instrument in instruments:
        if check_velocity_conditions(instrument['velocity'], v_avg):
            valid_instruments.append(instrument)

    score = len(valid_instruments) * 20
    return score, v_avg, instruments, valid_instruments

with open('children_population.json', 'r') as file:
    data = json.load(file)

for i, parent_data in enumerate(data):
    score, avg_velocity, all_instruments, valid_instruments = calculate_velocity_score(parent_data)
    print(f"\nParent {i+1}:")
    print(f"Average Velocity: {avg_velocity:.2f}")
    print("\nAll Instruments:")
    for inst in all_instruments:
        print(f"- {inst['category']}: {inst['velocity']}")
    print("\nValid Instruments:")
    for inst in valid_instruments:
        print(f"- {inst['category']}: {inst['velocity']}")
    print(f"Score: {score}")
    print("-" * 50)
