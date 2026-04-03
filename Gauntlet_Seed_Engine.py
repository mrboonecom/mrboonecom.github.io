import pandas as pd
import random
import os

def generate_gauntlet_seeds(total_batches=50, filename="seeds.xlsx"):
    """
    Generates deterministic Seed Codes for the Gauntlet-DB AI Prompt
    and exports them to an Excel file.
    """
    data = []
    
    # We gradually increase the root ranges as the batches get higher 
    # to naturally increase the difficulty and guarantee no overlap.
    for i in range(1, total_batches + 1):
        batch_number = i
        
        # Determine root ranges based on the batch progression
        if i <= 10:
            range_start, range_end = 1, 15
        elif i <= 30:
            range_start, range_end = 5, 25
        else:
            range_start, range_end = 10, 40
            
        # Generate a 4-digit random pin for entropy
        entropy_pin = random.randint(1000, 9999)
        
        # Construct the structured Seed Code
        seed_code = f"SEED-{entropy_pin}-R{range_start:02d}-{range_end:02d}"
        
        # The exact text you will copy-paste to the AI
        prompt_input = f"Batch Number: {batch_number} | Seed Code: {seed_code}"
        
        data.append({
            "Batch Number": batch_number,
            "Seed Code": seed_code,
            "Root Range": f"{range_start} to {range_end}",
            "Copy/Paste to AI": prompt_input
        })

    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Export to Excel
    try:
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"✅ Success! Generated {total_batches} batches.")
        print(f"📁 Saved as: {os.path.abspath(filename)}")
    except ImportError:
        print("❌ Error: Missing 'openpyxl' library.")
        print("Run 'pip install pandas openpyxl' in your terminal and try again.")

if __name__ == "__main__":
    print("🚀 Initializing Gauntlet Seed Engine...")
    
    # You can change the number of batches here
    BATCHES_TO_GENERATE = 20 
    
    generate_gauntlet_seeds(total_batches=BATCHES_TO_GENERATE)
