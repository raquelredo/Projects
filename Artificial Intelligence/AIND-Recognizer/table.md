
Word  |cross-validation   | BIC   | DIC
--|---|---|--
FISH | 3 - 0.0613|2 - 0.5759|2 - 0.5715
BOOK | 3 - 0.1466| 2 - 4.03846|2 - 3.5894
VEGETABLE | 3 - 0.0425| 2 - 1.2526|2 - 1.3929
FUTURE | 3 - 0.1370| 2 - 3.6267|2 - 3.8617
JOHN | 3 - 1.2676| 2 - 32.4580|2 - 37.4705

where x-y, x represents the number of hidden states and y the seconds of computation

  |features_ground    |features_norm   | feautures_polar  |  features_delta  |   feautures_custom
--|---|---|---|---|--
**SelectorConstant**  | WER = 0.6685393258426966 (Total correct: 59 out of 178)	|	WER = 0.6235955056179775 (Total correct: 67 out of 178)	|	WER = 0.6179775280898876 (Total correct: 68 out of 178)	|	WER = 0.6404494382022472 (Total correct: 64 out of 178)	|	WER = 0.8314606741573034 (Total correct: 30 out of 178)
**SelectorBIC**  |WER = 0.6348314606741573 (Total correct: 65 out of 178)	|	WER = 0.6629213483146067 (Total correct: 60 out of 178)	|	WER = 0.6404494382022472 (Total correct: 64 out of 178)	|	WER = 0.6067415730337079 (Total correct: 70 out of 178)	|	WER = 0.898876404494382 (Total correct: 18 out of 178)
 **SelectorDIC**  |WER = 0.6348314606741573 (Total correct: 65 out of 178)	|	WER = 0.6629213483146067 (Total correct: 60 out of 178)	|	WER = 0.6404494382022472 (Total correct: 64 out of 178)	|	WER = 0.6067415730337079 (Total correct: 70 out of 178)	|	WER = 0.898876404494382 (Total correct: 18 out of 178)
  **SelectorCV**  |WER = 0.6685393258426966 (Total correct: 59 out of 178)	|	WER = 0.6235955056179775 (Total correct: 67 out of 178)	|	WER = 0.6179775280898876 (Total correct: 68 out of 178)	|	WER = 0.6404494382022472 (Total correct: 64 out of 178)	|	 WER = 0.8314606741573034 (Total correct: 30 out of 178)
