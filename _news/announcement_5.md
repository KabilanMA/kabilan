---
layout: post
title: Presented a paper in APSEC-2024
date: 2024-12-05 11:59:00-0400
inline: false
related_posts: false
---

Presented the paper [BugsInKube: A Collection of Reconciliation Bugs](/../assets/pdf/BugsInKube.pdf) at APSEC 2024.

---

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="/../assets/img/apsec_2024/1.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="/../assets/img/apsec_2024/2.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="/../assets/img/apsec_2024/3.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="/../assets/img/apsec_2024/4.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

A dataset consisting of reconciliation bugs in Kubernetes and introduction to reconciliation bugs.

Paper Abstract:

In the contemporary technological landscape, the widespread adoption of cloud systems and distributed resources has highlighted the need to overcome inherent limitations in achieving complete system dependability. This presents both significant opportunities and challenges in automating bug detection, bug fixing, and verification efforts in complex distributed systems, such as cloud infrastructure management tools like Kubernetes and Twine. Despite the importance of these efforts, there is a notable lack of data that can be used to study and analyze the types of challenges faced in developing and supporting these systems, as well as in building test automation and bug detection tools. To address this gap, we conducted an in-depth investigation into one of the most popular ecosystems: Kubernetes. We manually analyzed reported bugs and curated a comprehensive dataset comprising 311 developer-confirmed bugs. This dataset includes detailed information on bug categories, severity, affected versions, and reproducible steps when available. Through our analysis, we identified an emerging bug type in these systems, referred to as reconciliation bugs. To assist developers and researchers in creating new testing strategies for these platforms, we developed a bug-reproducing script that can reproduce 52 reconciliation bugs out of the 311 total bugs in Kubernetes. This tool provides valuable insights into these issues, facilitating the development of more robust testing and maintenance strategies. The dataset is publicly available and can be accessed at: [https://github.com/EmInReLab/BugsInKube](https://github.com/EmInReLab/BugsInKube)

---
