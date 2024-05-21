import os
import argparse
import time
from rss_reader import fetch_feeds_from_file
from similarity_checker import group_similar_articles
from json_manager import save_grouped_articles


def main(similarity_threshold: float) -> None:
    """Main function to process RSS feeds and group similar articles."""
    print("Starting RSS feed processing...")
    input_file_path = 'input/feeds.txt'
    start_time = time.time()

    print("Fetching and parsing RSS feeds...")
    articles = fetch_feeds_from_file(input_file_path)
    print(f"Total articles fetched and parsed: {len(articles)}")

    print(f"Grouping articles based on similarity (threshold={similarity_threshold})...")
    grouped_articles = group_similar_articles(articles, similarity_threshold)
    print(f"Total groups formed: {len(grouped_articles)}")

    print("Saving grouped articles to JSON files...")
    group_sizes = save_grouped_articles(grouped_articles, 'output')
    total_files_saved = len(group_sizes)

    elapsed_time = time.time() - start_time
    print(f"RSS feed processing complete. {total_files_saved} different articles are now grouped.")
    print(f"Details of groups saved: {group_sizes}")
    print(f"(Took {elapsed_time:.2f} seconds)")

    # Additional output to summarize file generation
    print("Summarizing output files:")
    output_files = os.listdir('output')
    for filename in output_files:
        path = os.path.join('output', filename)
        with open(path, 'r', encoding='utf-8') as file:
            line_count = sum(1 for _ in file)
        print(f"{filename}: {line_count} lines")
    print(f"Total output files: {len(output_files)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process RSS feeds and group similar articles based on a similarity threshold.'
    )
    parser.add_argument(
        '-t', '--threshold', type=float, default=0.5,
        help='Set the similarity threshold for grouping articles (default: 0.5).'
    )
    args = parser.parse_args()
    main(args.threshold)
