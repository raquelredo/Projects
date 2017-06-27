
Lending Club
============

Dataset
-------

Dataset is public avalaible on the [site](https://www.lendingclub.com/). File can be found in the [input](../inputs/loan_data.csv) folder of this repo. It has been cleaned for NaN values.

It consists in values from calls to 911 for Monntgomery County, PA.

Database released under Open Database License, individual contents under Database Contents License

Description
-----------

Here are what the columns represent:

<table style="width:76%;">
<colgroup>
<col width="8%" />
<col width="68%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Variable</strong></th>
<th><strong>Definition</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>credit.policy</td>
<td>1 if the customer meets the credit underwriting criteria of LendingClub.com, and 0 otherwise.</td>
</tr>
<tr class="even">
<td>purpose</td>
<td>The purpose of the loan (takes values &quot;credit_card&quot;, &quot;debt_consolidation&quot;, &quot;educational&quot;, &quot;major_purchase&quot;, &quot;small_business&quot;, and &quot;all_other&quot;).</td>
</tr>
<tr class="odd">
<td>int.rate</td>
<td>The interest rate of the loan, as a proportion (a rate of 11% would be stored as 0.11). Borrowers judged by LendingClub.com to be more risky are assigned higher interest rates.</td>
</tr>
<tr class="even">
<td>installment</td>
<td>The monthly installments owed by the borrower if the loan is funded.</td>
</tr>
<tr class="odd">
<td>log.annual.inc</td>
<td>The natural log of the self-reported annual income of the borrower.</td>
</tr>
<tr class="even">
<td>dti</td>
<td>The debt-to-income ratio of the borrower (amount of debt divided by annual income).</td>
</tr>
<tr class="odd">
<td>fico</td>
<td>The FICO credit score of the borrower.</td>
</tr>
<tr class="even">
<td>days.with.cr.line</td>
<td>The number of days the borrower has had a credit line.</td>
</tr>
<tr class="odd">
<td>revol.bal</td>
<td>The borrower's revolving balance (amount unpaid at the end of the credit card billing cycle).</td>
</tr>
<tr class="even">
<td>revol.util</td>
<td>The borrower's revolving line utilization rate (the amount of the credit line used relative to total credit available).</td>
</tr>
<tr class="odd">
<td>inq.last.6mths</td>
<td>The borrower's number of inquiries by creditors in the last 6 months.</td>
</tr>
<tr class="even">
<td>delinq.2yrs</td>
<td>The number of times the borrower had been 30+ days past due on a payment in the past 2 years.</td>
</tr>
<tr class="odd">
<td>pub.rec</td>
<td>The borrower's number of derogatory public records (bankruptcy filings, tax liens, or judgments).</td>
</tr>
</tbody>
</table>
