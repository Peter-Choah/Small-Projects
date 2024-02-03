* Reading Products Table ;
proc import datafile = '/home/u48315265/Problem Solving Coursework/Products.csv'
	out = products
	dbms = csv
	replace;
	guessingrows = 100;
run;

* Reading Transactions Table ;
proc import datafile = '/home/u48315265/Problem Solving Coursework/Transactions.csv'
	out = transactions
	dbms = csv
	replace;
run;

* Customer table;
proc import datafile = '/home/u48315265/Problem Solving Coursework/Customer.csv'
	out = customer
	dbms = CSV
	replace;
run;

* Cleaning missing data ;
data customer;
	set customer;
	if city_code eq . then delete;
	if Gender eq '' then delete;
	Age = floor(yrdif(DOB, '31Dec2014'd));
run;

* Remove Duplicate Data ;
proc sort data=Transactions out=Transactions nodupkey dupout=duplicatetransactions;
	by transaction_id;
run;

* Merge Transactions & Products tables;
Proc sql;
    create table TransactionsMerge1 as 
    select *
    from Transactions join Products
    on Transactions.prod_cat_code = Products.prod_cat_code
    and Transactions.prod_subcat_code = Products.prod_sub_cat_code;
quit;

data TransactionsMerge;
	set TransactionsMerge1;
	Year = year(tran_date);
	Month = month(tran_date);
	Quarter = qtr(tran_date);
	drop prod_sub_cat_code;
run;

* Merge TP & Customer tables;
Proc sql;
	create table TPC1 as
	select *
	from TransactionsMerge left join customer
	on TransactionsMerge.cust_id = customer.customer_Id;
quit;

data TPC;
	set TPC1;
	drop customer_Id;
run;

* [A] Current Business Progress ;

* [1] Where Are Their Incomes Mainly Coming From? ;
* [1.1] Analysis on Product Categories ;

* Figure 1 ;
* Products Sold By Product Category ;
proc sgplot data = TransactionsMerge;
	vbar prod_cat;
	title 'Product Category';
	label prod_cat = 'Product Category';
run;

proc sort data = TransactionsMerge out = sorted_merged_prod;
	by prod_cat prod_subcat;
run;

data subprod;
	set sorted_merged_prod;
	by prod_cat prod_subcat;
	if first.prod_cat or first.prod_subcat then Total_Income = 0;
	if total_amt ge 0 then Total_Income + total_amt;
	if last.prod_subcat;
	keep prod_cat prod_subcat Total_Income;
run;

* Figure 2 ;
* Total Income by Product Category ;
proc sgplot data = subprod;
	vbar prod_cat / response = Total_Income;
	title 'Total Income by Product Category';
	format Total_Income dollar20.2;
	label Total_Income = 'Total Income' prod_cat = 'Product Category';
run;

* [1.2] Analysis on Product Subcategories ;

* Figure 3;
* Python code ;

* [1.3] Analysis on Product Categories Based on Time ;
proc sort data = TransactionsMerge out = sorted_merged_quarterprod;
	by Year Quarter prod_cat prod_subcat;
run;

data prodquarter;
	set sorted_merged_quarterprod;
	by Year Quarter prod_cat;
	if first.Quarter or first.prod_cat then Total_Income = 0;
	if total_amt ge 0 then Total_Income + total_amt;
	if last.prod_cat;
	keep Year Quarter prod_cat Total_Income;
run;

* Figure 4 ;
* Total Income per Quarter by Product Category ;
proc sgplot data = prodquarter;
	where Year ne 2014;
	vbar Quarter / response = Total_Income group = prod_cat groupdisplay = cluster nostatlabel;
	format Total_Income dollar20.2;
	title 'Total Income per Quarter by Product Category (2011 - 2013)';
	label Total_Income = 'Total Income' prod_cat = 'Product Category';
run;
title;

data subprodquarter;
	set sorted_merged_quarterprod;
	by Year Quarter prod_cat prod_subcat;
	if first.Quarter or first.prod_subcat then Total_Income = 0;
	if total_amt ge 0 then Total_Income + total_amt;
	if last.prod_subcat;
	keep Year Quarter prod_cat prod_subcat Total_Income;
run;

* Figure 5 ;
* Total Income per Quarter from Books ;
proc sgplot data = subprodquarter;
	where Year ne 2014 and prod_cat = 'Books';
	vbar Quarter / response = Total_Income group = prod_subcat groupdisplay = cluster nostatlabel;
	format Total_Income dollar20.2;
	title 'Total Income per Quarter from Books (2011 - 2013)';
	label Total_Income = 'Total Income' prod_subcat = 'Product Subcategory';
run;
title;

* Figure 6 ;
* Total Income per Quarter from Electronics ;
proc sgplot data = subprodquarter;
	where Year ne 2014 and prod_cat = 'Electronics';
	vbar Quarter / response = Total_Income group = prod_subcat groupdisplay = cluster nostatlabel;
	format Total_Income dollar20.2;
	title 'Total Income per Quarter from Electronics (2011 - 2013)';
	label Total_Income = 'Total Income' prod_subcat = 'Product Subcategory';
run;
title;

* [1.4] Analysis On Different Store Types ;

data TransactionsComplete;
	set TransactionsMerge;
	if prod_cat_code = 1 and prod_subcat_code = 4 then prod_subcat = "Clothing Mens";
	else if prod_cat_code = 1 and prod_subcat_code = 1 then prod_subcat = "Clothing Women";
	else if prod_cat_code = 1 and prod_subcat_code = 3 then prod_subcat = "Clothing Kids";
	else if prod_cat_code = 2 and prod_subcat_code = 1 then prod_subcat = "Footwear Mens";
	else if prod_cat_code = 2 and prod_subcat_code = 3 then prod_subcat = "Footwear Women";
	else if prod_cat_code = 2 and prod_subcat_code = 4 then prod_subcat = "Footwear Kids";
	else if prod_cat_code = 4 and prod_subcat_code = 1 then prod_subcat = "Bags Mens";
	else if prod_cat_code = 4 and prod_subcat_code = 4 then prod_subcat = "Bags Women";
run;

proc sort data=TransactionsComplete out=StoreTransactions;
	by Store_type prod_cat_code prod_subcat_code;
run;

data 	
	FullProductTransactions 
	returns_store 
	returns_cat 
	returns_subcat 
	transaction_totals ;

	set StoreTransactions end=last;
	by Store_type prod_cat_code prod_subcat_code;
	ratioaverage = 0.1112;
	store_frequency+1;
	
*set accumulating totals for income;
	if qty > 0 then do;
		Income = total_amt;
		cumulative_income + total_amt;
		qty_cumulative_income + qty;
		store_income + total_amt;
		qty_store + qty;
		category_income + total_amt;
		qty_category + qty;
		subcategory_income + total_amt;
		qty_subcategory + qty;
	end;
	
*set accumulating totals for returns;
	else do;
		Returns = abs(total_amt);
		cumulative_returns + abs(total_amt);
		qty_cumulative_returns + abs(qty);
		store_returns + abs(total_amt);
		qty_store_returns + abs(qty);
		category_returns + abs(total_amt);
		qty_category_returns + abs(qty);
		subcategory_returns + abs(total_amt);
		qty_subcategory_returns + abs(qty);
	end;
	
*output All;
output FullProductTransactions;

*subcategory (tertiary variable);
	if last.prod_subcat_code then do;
*output relevant information;
		returntoincome_subcategory = subcategory_returns / subcategory_income;
		qty_returntoincome_subcategory = qty_subcategory_returns / qty_subcategory;
		output returns_subcat;
*reset subcategory variables;
		subcategory_income = 0;
		qty_subcategory = 0;
		subcategory_returns = 0;
		qty_subcategory_returns = 0;
	end;
	
*category (secondary variable);
	if last.prod_cat_code then do;
*output relevant information;
		returntoincome_category = category_returns / category_income;
		qty_returntoincome_category = qty_category_returns / qty_category;
		output returns_cat;
*reset category variables;
		category_income = 0;
		qty_category = 0;
		category_returns = 0;
		qty_category_returns = 0;
	end;
	
*store type (primary variable);
	if last.Store_type then do;
		returntoincome_store = store_returns / store_income;
		qty_returntoincome_store = qty_store_returns / qty_store;
*store profit for eda;
		store_profit = store_income-store_returns;
		output returns_store;
*reset store variables;
		store_frequency = 0;
		store_income = 0;
		qty_store = 0;
		store_returns = 0;
		qty_store_returns = 0;
	end;
	
*output totals;
	if last then do;
		returntoincome_totals = cumulative_returns/cumulative_income;
		qty_returntoincome_totals = qty_cumulative_returns/qty_cumulative_income;
		output transaction_totals;
	end;
format 	cumulative_returns store_returns category_returns subcategory_returns cumulative_income store_income category_income subcategory_income dollar15.2 
		qty_store_returns qty_category_returns qty_subcategory_returns qty_store qty_category qty_subcategory comma.
		prod_cat_code CTG.
		;
label 	
		Store_type="Store Type"
		prod_cat_code="Product Category"
		prod_subcat = "Product Subcategory"
		cumulative_returns="Cumulative Returns"
		store_returns="Store Returns"
		qty_store_returns="Store Quantity Returned"
		category_returns="Category Returns"
		qty_category_returns="Category Quantity Returned"
		subcategory_returns = "Subcategory Returns"
		qty_subcategory_returns = "Subcategory Quantity Returned"
		returntoincome_store="Return to Income Ratio"
		qty_returntoincome_store="Quantity Ratio"
		returntoincome_category="Return to Income Ratio"
		qty_returntoincome_category="Quantity Ratio"
		returntoincome_subcategory="Return to Income Ratio"
		;	
run;

* Figure 7 ;
* Transaction Frequency by Store Type ;
proc sgplot data = TransactionsMerge;
	vbar store_type;
	title 'Transaction Frequency by Store Type ';
	label store_type = 'Store Types';
run;

* Figure 8 ;
* Store Profit by Store Type ;
proc sgplot data = returns_store;
	vbar store_type / response=store_profit;
	format store_profit dollar20.2;
	title 'Store Profit by Store type';
	label store_profit="Store Profit";
Run;

* [1.5] Analysis on Product Categories within each Store Type ;
proc sort data = TransactionsMerge out = sorted_merged_prodstore;
	by prod_cat store_type;
run;

data prodstore;
	set sorted_merged_prodstore;
	by prod_cat store_type;
	if first.prod_cat or first.store_type then Total_Income = 0;
	if total_amt ge 0 then Total_Income + total_amt;
	if last.store_type;
	keep prod_cat store_type prod_subcat prod_subcat2 Total_Income;
run;

* Figure 9 ;
* Total Income by Product Category and Store Type ;
proc sgplot data = prodstore;
	vbar store_type / response = Total_Income group = prod_cat groupdisplay = cluster nostatlabel;
	format Total_Income dollar20.2;
	title 'Total Income by Product Category and Store Type';
	label Total_Income = 'Total Income' prod_cat = 'Product Category' store_type = 'Store Type';
run;

* [2] Where/What is allowing them to make a big loss? ;
* [2.1] Income vs Loss of each store type ;

* Figure 10 ;
* Store Income by Store Type ;
proc sgplot data = returns_store;
	vbar store_type / response=store_income;
	title 'Store Income';
	label store_income="Store Income";
Run;

* Figure 11 ;
* Store Returns by Store Type ;
proc sgplot data = returns_store;
	vbar store_type / response=store_returns;
	title 'Store Returns';
	label store_returns="Store Returns";
Run;

* [2.2] Analysis of Product Category in each Store Type ;
*Figure 12
*ratio of return to income for each product category;
proc sgplot data = returns_cat;
	*where (if any);
	vbar store_type / response = returntoincome_category group = prod_cat_code groupdisplay = cluster ;
	title 'Return to Income Ratio of each Product category grouped by Store type';
	label ;
Run;
title;

* [2.3] Analysis on Product Subcategories in each Store Type ;
*Figure 13;
*ratio of return to income for each product category;
title "Return to Income Ratio of Product Subcategories grouped by Store Type";
footnote "Average Return to Income ratio is 0.11354.";
proc sgplot data=returns_subcat;
	vbar store_type / response=returntoincome_subcategory group = prod_subcat groupdisplay=cluster grouporder=data;
	vline store_type / response=ratioaverage  group=prod_subcat;
run;
title;
footnote;

*Figure 14;
title "Summarised Return to Income Ratio of Product Subcategories grouped by Store Type";
footnote "Only product subcategories with 0.11354 return to income ratio are presented";
proc sgpanel data=returns_subcat;
panelby store_type;
	where returntoincome_subcategory >= 0.11354;
	vbar prod_cat_code / response=returntoincome_subcategory group = prod_subcat groupdisplay=cluster 
	grouporder=ascending ;
run;
footnote;
title;

* [B] Target Market ;

* [1] Which market contributes the most to company XYZ over the years? [Demographics] ;
* [1.1] Which generation is the most popular one? ;
data age;
	set TPC;
	if 6 <= Age <= 24
		then group = 'Gen Z';
	else if 25 <= Age <= 40
		then group = 'Gen Y';
	else if 41 <= Age <= 56
		then group = 'Gen X';
	else if 57 <= Age <= 75
		then group = 'BabyBoomers';
run;

* Figure 15 ;
* Proportion of Company XYZ’s Customers by Generation ;
title 'Age Groups';
proc gchart data=age;
	pie3d group / type = freq
	value=arrow
	percent=inside
	plabel=(font='Albany AMT/bold' h=2 )
	slice=inside
	explode = 'Gen Y' 'Gen Z' 'Gen X';
run;
title;

* [1.2] In that generation, which gender contributes the most? ;
data byage;
	set age;
	if group ne "Gen Y" then delete;
run;

* Figure 16 ;
* Proportion of Company XYZ’s Customers by Gender ;
title 'Gender Groups';
proc gchart data=byage;
   pie3d gender / type = freq
                value=arrow
                percent=inside
                plabel=(font='Albany AMT/bold' h=2 )
                slice=inside
                explode = 'M';
run;
title;

* [1.3] In that gender category, where are they mostly located? ;
data bygender1;
	set byage;
	if gender ne "M" then delete;
run;

* Proportion;
proc freq data = bygender1 order = data;
	tables city_code * Gender / chisq out = test1;
run;

data bygender2;
	set byage;
	if gender ne "F" then delete;
run;

* Proportion ;
proc freq data = bygender2 order = data;
	tables city_code * Gender / chisq out = test2;
run;

*Merge test 1 & 2;
data yes1;
	merge test1 test2;
	by Gender;
run;

* Figure 17 ;
* Proportion of Generation Y’s Genders by City Code ;
proc sgplot data = yes1;
	vbar city_code / response = percent
	group = gender
	groupdisplay = cluster;
	title 'City Codes for Males & Females';
run;

* [1.4] In that city code, what stores are available? [Availability of stores - Easy Access] ;
data bycitycode1;
	set bygender1;
	if city_code ne 8 then delete;
run;

* Proportion;
proc freq data = bycitycode1 order = data;
	tables store_type * Gender / chisq out = test3;
run;


data bycitycode2;
	set bygender2;
	if city_code ne 1 then delete;
run;

* Proportion;
proc freq data = bycitycode2 order = data;
	tables store_type * Gender / chisq out = test4;
run;

*Merge test 3 & 4;
data yes2;
	merge test3 test4;
	by Gender;
run;

* Figure 18 ;
* Proportion of Generation Y’s Genders by Store Type ;
proc sgplot data = yes2;
	vbar store_type / response = percent
	group = gender
	groupdisplay = cluster;
	*dataskin = gloss;
	title 'Store Type in City Codes for Males & Females';
run;

* [1.5] In that store, what is the most preferred product category bought? ;
data bystoretype1;
	set bycitycode1;
	if store_type ne "e-Shop" then delete;
run;

* Proportion;
proc freq data = bystoretype1 order = data;
	tables prod_cat * Gender / chisq out = test5;
run;

data bystoretype2;
	set bycitycode2;
	if store_type ne "e-Shop" then delete;
run;

* Proportion;
proc freq data = bystoretype2 order = data;
	tables prod_cat * Gender / chisq out = test6;
run;

*Merge test 5 & 6;
data yes3;
	merge test5 test6;
	by Gender;
run;

* Figure 19 ;
* Proportion of Gen Y’s Genders by Product Categories in e-Shops ;
proc sgplot data = yes3;
	vbar prod_cat / response = percent
	group = gender
	groupdisplay = cluster;
	*dataskin = gloss;
	title 'Product Category Store Type in City Codes for Males & Females';
run;

* [1.6] In that product category, what is the most preferred product sub-category bought? ;
data byproduct1;
	set bystoretype1;
	if prod_cat ne "Books" then delete;
run;

* Proportion;
proc freq data = byproduct1 order = data;
	tables prod_subcat * Gender / chisq out = test7;
run;

data byproduct2;
	set bystoretype2;
	if prod_cat ne "Books" then delete;
run;

* Proportion;
proc freq data = byproduct2 order = data;
	tables prod_subcat * Gender / chisq out = test8;
run;

*Merge test 7 & 8;
data yes4;
	merge test7 test8;
	by Gender;
run;

* Figure 20 ;
* Proportion of Gen Y’s Genders by Product Subcategories for Books in e-Shops ; 
proc sgplot data = yes4;
	vbar prod_subcat / response = percent
	group = gender
	groupdisplay = cluster;
	*dataskin = gloss;
	title 'Product Sub-category of the Product Category in Store Type in City Codes for Males & Females';
run;


* APPENDIX II ;

*Figure 21;
*Descriptive statistics for Income;
title "Distribution of Income";
proc univariate data=FullProductTransactions;
	var income;
	histogram;
run;

*Figure 22;
*Descriptive statistics for returns;
title "Distribution of Returns";
proc univariate data=FullProductTransactions;
	var returns;
	histogram;
run;


* APPENDIX III ;
* Figure 23 ;
*Returns of each Product category grouped by Store type;
proc sgplot data = returns_cat;
	*where (if any);
	vbar store_type / response = category_returns group = prod_cat_code groupdisplay = cluster ;
	title 'Returns of each Product category grouped by Store type';
	label ;
run;

* APPENDIX IV ;
proc sort data = TransactionsMerge out = sorted_merged_storeprod;
	by store_type prod_cat prod_subcat;
run;

data prodstore;
	set sorted_merged_storeprod;
	by store_type prod_cat;
	if first.prod_cat or first.store_type then do;
		Total_Income = 0;
		total_qty = 0;
	end;
	if total_amt ge 0 then do;
		Total_Income + total_amt;
		total_qty + Qty;
	end;
	if last.prod_cat then AvgPricePerProduct = Total_Income/total_qty;
	if last.prod_cat;
	keep prod_cat store_type total_qty AvgPricePerProduct Total_Income;
run;

* Table 1 ;
* Average Price per Product in each Product Category within each Store Type ;
proc print data = prodstore label noobs;
	label Store_type = 'Store Type' prod_cat = 'Product Category' Total_Income = 'Total Income' 
	total_qty = 'Total Quantity' AvgPricePerProduct = 'Average Price per Product';
	format Total_Income AvgPricePerProduct dollar20.2;
run;

*Table 3;
*Printing totals in a table form;
title "Income and Returns";
footnote1 "Total Ratio is the ratio of Returns to Income";
proc print data=transaction_totals label;
var cumulative_income cumulative_returns returntoincome_totals ;
label 	cumulative_income = "Income"
		cumulative_returns = "Returns"
		returntoincome_totals = "Income to Return Ratio";
run;
title;
footnote;
