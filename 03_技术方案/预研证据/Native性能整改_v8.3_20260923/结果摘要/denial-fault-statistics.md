# 拒绝与故障单独统计

仅两真实宿主API进程上的顺序功能回归，不是限配并发窗口；不并入成功查询性能。每阶段16个状态均核对；3个worker响应不含elapsedMs，未伪造耗时，表中p95仅针对有计时样本。故障阶段冷热独立，另列全选定403总体，不给缺少标签的403推断缓存温度。

|候选|阶段|样本/有计时|状态分布|服务端p50 ms|服务端p95 ms|
|---|---|---:|---|---:|---:|
|1|warm protected controls|16/13|{200: 16}|17.664|37.622|
|1|Redis timeout warm|16/13|{503: 16}|311.002|321.593|
|1|Redis timeout cold restarted process|16/13|{503: 16}|313.587|328.157|
|1|Redis timeout recovery current authority|16/13|{200: 16}|21.930|34.876|
|1|Redis timeout cold process recovery current authority|16/13|{200: 16}|17.509|26.108|
|1|Redis disconnected warm|16/13|{503: 16}|3.802|6.130|
|1|Redis disconnected cold restarted process|16/13|{503: 16}|6.024|26.700|
|1|Redis reconnected current authority|16/13|{200: 16}|13.391|19.461|
|1|DB authority unavailable|16/13|{503: 16}|0.254|0.809|
|1|DB recovered authoritative current state|16/13|{200: 16}|14.408|24.706|
|1|全部选定预期403（混合路径/缓存）|97/94|403|9.465|26.796|
|2|warm protected controls|16/13|{200: 16}|16.843|33.402|
|2|Redis timeout warm|16/13|{503: 16}|308.620|315.954|
|2|Redis timeout cold restarted process|16/13|{503: 16}|311.590|323.119|
|2|Redis timeout recovery current authority|16/13|{200: 16}|18.329|33.449|
|2|Redis timeout cold process recovery current authority|16/13|{200: 16}|17.884|28.156|
|2|Redis disconnected warm|16/13|{503: 16}|3.197|5.885|
|2|Redis disconnected cold restarted process|16/13|{503: 16}|5.005|22.035|
|2|Redis reconnected current authority|16/13|{200: 16}|14.002|19.782|
|2|DB authority unavailable|16/13|{503: 16}|0.227|1.124|
|2|DB recovered authoritative current state|16/13|{200: 16}|16.784|22.466|
|2|全部选定预期403（混合路径/缓存）|97/94|403|8.247|27.115|
