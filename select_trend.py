
from pytrends.request import TrendReq
import tabulate


# Get Google Hot Trends data
def get_trends(pytrend):
    pytrend.build_payload(kw_list=['f'], timeframe='now 7-d', gprop='youtube')
    trending_searches_df = pytrend.trending_searches(pn='united_states')
    print("\n\nTrending Searches on YouTube:\n")
    print(tabulate.tabulate(trending_searches_df, headers=['Index', 'Trend'], tablefmt='grid'))
    return trending_searches_df


# Select the trend you want
def get_input(df):
    while True:  # Keep asking until valid input is received
        try:
            input_topic = input("Enter the index of the trend you want to select, or type your own topic: ")
            if len(input_topic) > 2:  # Consider it as a custom topic
                return input_topic
            else:  # Assume it's an index
                index = int(input_topic)
                if 0 <= index < len(df):
                    value = df.iat[index, 0]
                    return value
                else:
                    print(f"Please enter a number between 0 and {len(df) - 1}.")
        except ValueError:
            print(f"Invalid input. Please enter a number between 0 and {len(df) - 1}.")


# Get Google Keyword Suggestions
def get_keywords(value):
    pytrend = TrendReq()
    try:
        keywords = ["Shorts"]
        suggestions_dict = pytrend.suggestions(keyword=value)
        for i in range(0, len(suggestions_dict)):
            dict = suggestions_dict[i]
            for key, values in dict.items():
                if key == 'title' or key == 'type':
                    keywords.append(values)
    except Exception as e:
        print(f"An error occurred while fetching keyword suggestions: {e}")
    print(f"\nTags:\n\n{keywords}")
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


# Main method
def display_trend_and_get_input():
    pytrend = TrendReq()
    df = get_trends(pytrend)
    return get_input(df)
    

if __name__ == "__main__":
    display_trend_and_get_input()