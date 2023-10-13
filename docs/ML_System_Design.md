# ML System Design Document - Demand Forecast

## 1. Problem definition
### 1.1. Origin
Supermegaretaillite is a marketplace that encompasses thousands of consumer and office electronics products. These categories have their unique characteristics, demand, and supply cycles, which need to be taken into consideration by category managers when planning purchases. Before selling any product, Supermegaretaillite must purchase it in the necessary volumes from the supplier. Due to limited warehouse space, the category manager needs to consider several important aspects when purchasing a product:
    *Out-of-stock: This is when there is no required product left in the warehouse, and the next delivery is still a few days away. Consequently, the customer goes to competitors for their purchase, resulting in missed profits.
    Overstock: This is when a product "lingers" and does not sell we have to "liquidate" it by significantly reducing the price and selling below cost, just so it does not take up warehouse space.
    Missed profits: This is the lost revenue due to out-of-stock situations.
    Product turnover: This is how much time passes from the delivery of a unit of product to dispatch to a customer.*

The project goal of this ML service is to increase the profits of Supermegaretaillite and optimize the work of category
managers, as at the moment their approach involves calculating the average product sales over the last
n-days and multiplying by the number of days for which the purchase is made - this method does not take
into account seasonality, demand, and supply history. Considering this,
the management of Supermegaretaillite has decided to invest funds in the development of an automated procurement
management system from suppliers, which includes the development of an ML service for demand forecasting."
