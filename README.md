# Basketball Play Sequencing Research

## Data Issues
### NCAA Play-by-Play Data
* Free throw shots are not recorded in exact order.  During any given trip to the free throw line, misses are recorded first and makes are recorded second in the play logs.  For example, if a player makes the first FT and misses the second, it will appear the same as a trip where the first FT is missed and the second is made.  This prevents any analysis or breakdown that distiguished between the sequence of FT makes and misses.  Therefore a possession that results solely in FTA (i.e. not an and-1) will be classified only on the basis of attempts and makes.

## Built With

* [Pandas](https://pandas.pydata.org/) - Used for data analysis

## Authors

* **Ethan Carpenter**
* [GitHub](https://github.com/ethan9carpenter)
* [LinkedIn](https://www.linkedin.com/in/ethan-c-90870a11b/)
