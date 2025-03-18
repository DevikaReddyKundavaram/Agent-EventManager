import pandas as pd
import random
from fpdf import FPDF

# Load dataset
try:
    dataset = pd.read_csv('game_ideas.csv', quotechar='"')
    print("✅ Dataset loaded successfully!")
except Exception as e:
    print(f"❌ Error loading dataset: {e}")
    exit()

# PDF Class
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Event Game Plan', ln=True, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def filter_game(occasion, genre, game_type, age_group, difficulty):
    filtered = dataset[
        (dataset['occasion'].str.lower() == occasion.lower()) &
        (dataset['genre'].str.lower() == genre.lower()) &
        (dataset['game_type'].str.lower() == game_type.lower()) &
        ((dataset['age_group'].str.lower() == age_group.lower()) | (dataset['age_group'].str.lower() == 'all')) &
        (dataset['difficulty'].str.lower() == difficulty.lower())
    ]
    if not filtered.empty:
        return filtered.sample(1).iloc[0]
    else:
        print("⚠️ No exact game found. Fetching a random fallback game...")
        return dataset.sample(1).iloc[0]

def plan_event(total_minutes, occasion, genre, game_type, age_group, difficulty):
    event_plan = []
    time_per_game = 15  # Adjust based on your preference
    num_games = total_minutes // time_per_game

    for _ in range(num_games):
        game = filter_game(occasion, genre, game_type, age_group, difficulty)
        event_plan.append({
            'game': game['game_description'],
            'items': game['items_needed'],
            'difficulty': game['difficulty']
        })

    return event_plan

def generate_pdf(event_plan):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for idx, game in enumerate(event_plan, 1):
        pdf.multi_cell(0, 10, f"{idx}. {game['game']}\nItems: {game['items']}\nDifficulty: {game['difficulty']}\n", align='L')

    output_file = "event_plan.pdf"
    pdf.output(output_file)
    print(f"✅ Event plan PDF saved as {output_file}")

if __name__ == "__main__":
    print("\n🎉 Welcome to AI Event Game Planner 🎉\n")
    occasion = input("Enter Occasion (family, wedding, birthday, festival, corporate): ").strip()
    genre = input("Enter Genre (fun, bollywood, sangeet, team-building): ").strip()
    game_type = input("Enter Game Type (quiz, activity, charades, dance-off): ").strip()
    age_group = input("Enter Age Group (kids, adults, all): ").strip()
    difficulty = input("Enter Difficulty (easy, medium, hard): ").strip()

    # Single game suggestion
    selected_game = filter_game(occasion, genre, game_type, age_group, difficulty)
    print("\n🎯 Suggested Game Idea:")
    print(f"Game: {selected_game['game_description']}")
    print(f"Items Needed: {selected_game['items_needed']}")
    print(f"Difficulty: {selected_game['difficulty']}")

    # Event planning
    event_choice = input("\nDo you want to plan a full event? (yes/no): ").strip().lower()
    if event_choice == 'yes':
        total_duration = int(input("Enter total event duration in minutes: "))
        event_plan = plan_event(total_duration, occasion, genre, game_type, age_group, difficulty)

        print("\n📋 Event Schedule:")
        for idx, game in enumerate(event_plan, 1):
            print(f"{idx}. {game['game']} | Items: {game['items']} | Difficulty: {game['difficulty']}")

        # PDF generation
        generate_pdf(event_plan)
