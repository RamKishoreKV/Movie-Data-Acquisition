# Movie Data Acquisition and Analysis

This repository contains a Python project designed to collect, process, and analyze movie data from Wikipedia and The Movie Database (TMDb) API. The project focuses on extracting key information about movies, including financial performance, critical ratings, and personnel (directors and actors), to identify trends and insights within the film industry. This work was completed as part of a Data Science (DSCI) final project.

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Data Acquisition Process](#data-acquisition-process)
- [Technologies and Tools](#technologies-and-tools)
- [Data Sources](#data-sources)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Analysis Highlights](#analysis-highlights)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About the Project

This project addresses the challenge of gathering comprehensive movie data from disparate sources and transforming it into a structured format for analysis. It employs web scraping techniques for Wikipedia and API calls for TMDb to build a rich dataset. The subsequent analysis identifies top performers among directors and actors based on profitability, critical reception, and volume of work, and visualizes genre distribution. This repository also includes the final project presentation and scoping document from the DSCI course.
### 📁 Project Directory Structure

- `DSCI Final Project Presentation.pptx` – Final project presentation slides  
- `DSCI511 - Project Scoping (1).docx` – Project scoping document  
- `all_movies.json` – Primary JSON file containing scraped and processed movie data  
- `all_movies_backup.json` – Backup of the movie data  
- `final_project.ipynb` – Jupyter Notebook with acquisition, processing, and analysis  
- `final_project.py` – Core logic in Python script format  
- `readable_all_movies.json` – Human-readable version of JSON data  
- `top_genres_distribution.png` – Genre distribution pie chart  
- `budget_vs_revenue_scatter.png` – Budget vs. revenue scatter plot  
- `README.md` – This file  



## Features

- **Wikipedia Data Acquisition:** Scrapes movie plots and key information (director, cast, country, language, budget, box office, runtime) from Wikipedia pages.
- **TMDb API Integration:** Fetches additional movie details (vote average, vote count, overview, release date, runtime, genres) from The Movie Database API.
- **Data Harmonization:** Combines data from both sources into a unified JSON format (`all_movies.json` and `readable_all_movies.json`).
- **Financial Analysis:** Calculates profitability for directors and actors based on budget and box office revenue.
- **Performance Rating Analysis:** Determines top-rated directors and actors based on movie vote averages and counts.
- **Productivity Analysis:** Identifies actors with the most movie appearances.
- **Genre Distribution:** Visualizes the distribution of movie genres using a pie chart.
- **Numerical Feature Statistics:** Provides statistical summaries (mean, median, max, min, standard deviation) for quantitative movie attributes.

## Data Acquisition Process

The data collection process involves a multi-step approach to ensure comprehensive and relevant movie information is gathered:

1.  **Initial Movie Discovery (TMDb API):**
    * The project begins by querying The Movie Database (TMDb) API's `discover/movie` endpoint.
    * Movies are filtered based on specific criteria:
        * Language: English (`en-US`)
        * Release Date: On or after January 1st, 2010 (`primary_release_date.gte=2010-01-01`)
        * Vote Count: At least 100 votes (`vote_count.gte=100`)
        * Original Language: English (`with_original_language=en`)
        * Sorting: By popularity in descending order (`sort_by=popularity.desc`)
    * The total number of pages matching these criteria is determined, and an `all_movies` list is populated with movie titles and their corresponding TMDb IDs. This process is currently limited to a certain number of pages (e.g., 300) to manage runtime.

2.  **Detailed Movie Information (TMDb API):**
    * For each movie ID obtained in the discovery phase, a detailed API call is made to the `movie/{id}` endpoint.
    * This step retrieves features such as `vote_average`, `vote_count`, `overview`, `release_date`, `runtime`, and `genres`.

3.  **Wikipedia Web Scraping:**
    * For each movie, the project attempts to scrape additional information from its Wikipedia page using `BeautifulSoup`.
    * Multiple URL patterns are attempted for Wikipedia pages to account for common naming conventions:
        * Standard title: `Movie_Title`
        * Film disambiguation: `Movie_Title_(film)`
        * Year disambiguation: `Movie_Title_(Release_Year_film)` (using the release year from TMDb)
    * From Wikipedia, the script extracts "Plot" and details from the infobox, including "Directed by", "Screenplay by", "Produced by", "Starring", "Country", "Language", "Budget", and "Box office".
    * Numerical values for "Budget", "Box office", and "Running time" are parsed, handling different formats (e.g., millions, billions, ranges) and defaulting to TMDb data if Wikipedia parsing fails.

4.  **Data Consolidation and Storage:**
    * Information from Wikipedia and TMDb is combined into a single dictionary for each movie.
    * The complete dataset of movie dictionaries is then saved as a JSON file (`all_movies.json`).

**Note on Runtime:** The entire data acquisition process, especially the web scraping part, can be lengthy, taking approximately **1-2 hours** to run from scratch due to numerous API calls and web requests, and built-in `time.sleep()` to respect API rate limits.

## Sample Data Acquisition Output:
The final output of the data acquisition process is stored in the all_movies.json file, which contains detailed information for each movie, including both Wikipedia and TMDb data.

📂 Due to its large size, GitHub may not render the full content of all_movies.json in the browser.
📥 To explore the complete dataset, please download the file manually from the repository.

Here is a sample preview of the JSON structure and contents:

![Sample Output Snapshot](json_movies.png)



## Technologies and Tools

-   **Python 3.x:** The primary programming language used for the project.
-   **`requests`:** Used for making HTTP requests to Wikipedia's API and TMDb API.
-   **`BeautifulSoup4` (bs4):** A Python library for parsing HTML and XML documents, used for web scraping Wikipedia.
-   **`json`:** For handling JSON data, including loading and saving the processed movie data.
-   **`pandas`:** Utilized for data manipulation and analysis, especially for creating DataFrames for statistical calculations.
-   **`numpy`:** Provides support for numerical operations, particularly for handling `NaN` values in statistical analysis.
-   **`matplotlib.pyplot`:** Used for creating static, interactive, and animated visualizations, specifically for the genre distribution pie chart and the budget vs. revenue scatter plot.
-   **Jupyter Notebook (`.ipynb`):** The development environment where the code was written, executed, and documented (`final_project.ipynb`).
-   **Python Script (`.py`):** Contains the core logic, likely optimized for execution (`final_project.py`).
-   **The Movie Database (TMDb) API:** External API used to fetch supplementary movie data.
-   **Wikipedia API (RESTBase):** Used for programmatic access to Wikipedia content.

## Data Sources

The project leverages two primary data sources:

-   **Wikipedia:** For comprehensive movie information often presented in infoboxes and the "Plot" section.
-   **The Movie Database (TMDb) API:** For structured data points like vote averages, vote counts, and genre classifications.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

-   Python 3.x installed on your system.
-   An API key from The Movie Database (TMDb). You can obtain one by registering on their [website](https://www.themoviedb.org/documentation/api).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/RamKishoreKV/Movie-Data-Acquisition.git](https://github.com/RamKishoreKV/Movie-Data-Acquisition.git)
    cd Movie-Data-Acquisition
    ```

2.  **Install the required Python packages:**
    ```bash
    pip install requests beautifulsoup4 pandas numpy matplotlib
    ```

### Usage

1.  **Obtain your TMDb API Key:**
    -   Register at [The Movie Database](https://www.themoviedb.org/documentation/api) to get your API key.

2.  **Update API Key in the Notebook/Script:**
    -   Open `final_project.ipynb` or `final_project.py` in a Jupyter environment or your preferred text editor.
    -   Locate the API key placeholder (e.g., `Authorization: "Bearer YOUR_TMDB_API_READ_ACCESS_TOKEN_HERE"`) and replace it with your actual TMDb API read access token.
        *(Note: The provided `final_project.ipynb` shows `Authorization: "xxxx"` and `api_key = "d985e895dd723bde9097eb4dfa4f3a75"`. Ensure you update the `Authorization` header with your **Bearer** token for API requests to function correctly.)*

3.  **Run the Jupyter Notebook or Python Script:**
    -   **Jupyter Notebook:** Open `final_project.ipynb` in a Jupyter environment and execute all cells sequentially.
    -   **Python Script:** From your terminal, navigate to the project directory and run:
        ```bash
        python final_project.py
        ```
    -   **Important Note:** The data acquisition phase is time-consuming and may take **1-2 hours** to run from scratch. If `all_movies.json` is already present in the repository, the script might skip this step or use the existing data.

## Analysis Highlights

The analysis section provides key insights derived from the movie dataset:

-   **Top Profitable Directors and Actors:** Identifies individuals whose movies have generated the highest average profit, highlighting their commercial success.
-   **Top Best-Rated Directors and Actors:** Showcases those consistently involved in critically acclaimed films, based on vote averages and counts.
-   **Most Prolific Actors:** Lists actors with the highest number of movie appearances in the dataset, indicating their activity in the industry.

Beyond individual performance metrics, the project also provides visual and statistical analyses of the broader dataset:

### Genre Distribution

The pie chart below illustrates the proportional representation of different movie genres within the collected dataset. This helps in understanding which genres are most prevalent among English-language films released since 2010 with at least 100 votes.

![Top Genres Distribution Pie Chart](top_genres_distribution.png)
*(As seen in the example visualization, "Other" and "Drama" tend to be significant categories, followed by "Comedy" and "Thriller".)*

### Budget vs. Box Office Revenues

This scatter plot explores the relationship between a movie's production budget and its total box office revenue. It helps in identifying potential correlations between investment and financial return, as well as highlighting high-performing outliers or films with disproportionate success.

![Movie Budgets vs. Box Office Revenues Scatter Plot](budget_vs_revenue_scatter.png)
*(The plot generally shows that higher budgets correlate with higher revenues, but with considerable variability. There are also notable outliers indicating films that achieved very high box office success with varying budget levels.)*

### Numerical Feature Statistics

Finally, comprehensive statistical summaries (mean, median, max, min, standard deviation) are provided for quantitative movie attributes such as `budget`, `box_office`, `vote_average`, `vote_count`, and `runtime`. This offers a foundational understanding of the central tendencies and spread of these key numerical features across the dataset.

## 🔗 Related Projects
### 🔄 Further Analysis & Applications

While this repository provides a comprehensive pipeline for acquiring modern movie data (2010 onward), we used a **different version of the dataset** for further analysis — specifically focusing on **American movies released between 1950 and 2010**. This was done to explore long-term industry trends and historical patterns.

📂 **Explore the companion repository here:**  
🔗 [👉 Movie Database Analysis Repository](https://github.com/RamKishoreKV/Movie-Database-Analysis)

That project includes:
- NLP-based genre prediction (spaCy + TF-IDF)
- Content-based recommendation system
- Actor–Director collaboration network graphs
- Genre and popularity trend visualizations
- Financial and critical performance breakdowns

Together, both repositories form a complete movie intelligence system — from raw data acquisition to advanced insights and recommendation modeling.


## Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

## Contact

Ram Kishore KV - [rk999@drexel.edu]
Project Link: [https://github.com/RamKishoreKV/Movie-Data-Acquisition](https://github.com/RamKishoreKV/Movie-Data-Acquisition)
