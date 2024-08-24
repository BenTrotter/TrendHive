from pytrends.request import TrendReq
import tabulate

# Get Google Hot Trends data
def get_trends(pytrend):
    pytrend.build_payload(kw_list=['f'], timeframe='now 7-d', gprop='youtube')
    trending_searches_df = pytrend.trending_searches(pn='united_states')
    print("Trending Searches on YouTube:")
    print(tabulate.tabulate(trending_searches_df, headers=['Index', 'Trend'], tablefmt='grid'))
    return trending_searches_df

# Select the trend you want
def select_trend(df):
    while True:  # Keep asking until valid input is received
        try:
            index = int(input("Enter the index of the trend you want to select (0-4): "))
            if 0 <= index < len(df):
                value = df.iat[index, 0]
                print(f"Selected Trend: {value}")
                return value
            else:
                print("Please enter a number between 0 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 4.")

# Get Google Keyword Suggestions
def get_keywords(pytrend, value):
    try:
        keywords = []
        suggestions_dict = pytrend.suggestions(keyword=value)
        print("Keyword Suggestions:")
        headers = suggestions_dict[0].keys()  # Get the headers from the dictionary keys
        rows = [suggestion.values() for suggestion in suggestions_dict]
        print(tabulate.tabulate(rows, headers=headers, tablefmt='grid'))
        for i in range(0, len(suggestions_dict)):
            dict = suggestions_dict[i]
            for key, values in dict.items():
                if key == 'title' or key == 'type':
                    keywords.append(values)
    except Exception as e:
        print(f"An error occurred while fetching keyword suggestions: {e}")
    return limit_unique_strings_to_500(keywords)

# Limit keywords length and ensure no duplicates
def limit_unique_strings_to_500(strings):
    total_length = 0
    result = []
    seen = set()  # To track unique strings
    
    for string in strings:
        if string not in seen and total_length + len(string) <= 500:
            result.append(string)
            seen.add(string)  # Mark this string as seen
            total_length += len(string)
        elif total_length + len(string) > 500:
            break  # Stop if adding this string would exceed the limit
    
    return result


def display_select_trend():
    pytrend = TrendReq()
    trends_df = get_trends(pytrend)
    selected_trend = select_trend(trends_df)
    keywords = get_keywords(pytrend, selected_trend)
    print("Keywords: \n", keywords)

if __name__ == "__main__":
    display_select_trend()