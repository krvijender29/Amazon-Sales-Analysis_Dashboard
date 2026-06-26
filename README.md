# 📦 Amazon Sales Analysis Dashboard

An interactive **Streamlit** dashboard built on top of an Amazon product sales dataset analysis (converted from a Jupyter Notebook EDA project). It visualizes pricing, discounts, ratings, and category-level performance through clean, interactive charts and KPIs.

🔗 **Live Demo:** [Click here to view the live app](https://amazon-sales-analysisdashboard-3ukwibdumnb2mcviccxrxp.streamlit.app/) <!-- TODO: replace with your actual deployed link -->

---

## ✨ Features

- 📊 **KPI Cards** — Total Products, Average Discount, Average Rating, Total Reviews, Rating↔Discount Correlation
- 🔥 **Top 10 Most Reviewed Products**
- ⭐ **Category-wise Average Rating**
- 💸 **Category-wise Average Discount**
- 📈 **Product Count by Category** (pie chart)
- 📉 **Rating Distribution** histogram
- 🔍 **Rating vs Discount Percentage** scatter plot with correlation
- 🏆 **Top Products by Performance Score** (`rating × log(1 + rating_count)`)
- 💎 **Most Expensive** & 🪙 **Cheapest** product tables
- 🎛️ **Sidebar Filters** — category, rating range, price range
- 📄 Expandable raw/filtered data table

---

## 🗂️ Project Structure

```
.
├── main.py   # Main Streamlit app
├── requirements.txt           
├── Charts
    ├── Rating-Distribution-plot.png
    └── Rating-VS-Discount-plot.png
├── Notebook
    └── amazon-sales-analysis-notebook.csv
├── Data/
│   └── amazon.csv             
└── README.md
```

---

## 📋 Dataset

The app expects a CSV file with at least the following columns:

| Column                | Description                          |
|------------------------|---------------------------------------|
| `product_id`           | Unique product identifier             |
| `product_name`         | Product title                         |
| `category`             | Product category (path-style string)  |
| `discounted_price`     | Price after discount (e.g. `₹1,099`)  |
| `actual_price`         | Original price (e.g. `₹1,999`)        |
| `discount_percentage`  | Discount percent (e.g. `45%`)         |
| `rating`               | Product rating (e.g. `4.2`)           |
| `rating_count`         | Number of ratings/reviews             |

---


## 🚀 Deployment

This app can be deployed for free on **[Streamlit Community Cloud](https://streamlit.io/cloud)**:

1. Push this project to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo.
3. Set the main file path to `amazon_sales_dashboard.py`.
4. Make sure `Data/amazon.csv` is included in the repo (or hosted accessibly), then deploy.

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — app framework
- [Pandas](https://pandas.pydata.org/) / [NumPy](https://numpy.org/) — data processing
- [Plotly](https://plotly.com/python/) — interactive visualizations

---

## 📄 License

This project is open-sourced for learning and portfolio purposes. Feel free to fork and adapt it.

---

## 🙋 Author

Built as a data analysis & dashboarding portfolio project. Contributions and suggestions are welcome via issues or pull requests.