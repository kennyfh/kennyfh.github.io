---
title: "Dossier CAUS - Competitive Programming Template"
tags: [Typst, CI/CD, Automation, Competitive Programming, Python, C++]
externalUrl: ""
weight: 1
showDate: false
showAuthor: false
showReadingTime: false
showEdit: false
showLikes: false
showViews: false
layoutBackgroundHeaderSpace: false
showTableOfContents : false
showWordCount : false
---

{{< alert >}}
You can access the resource using the following link: [Download here](https://github.com/algoritmiaUS/dossier-template/releases/tag/v1.0.0)
{{</ alert >}}


### **Project Overview**

This project provides the official, high-performance dossier template for the **Club de Algoritmia de la Universidad de Sevilla (CAUS)**. Developed as a modern alternative to traditional LaTeX templates, it utilizes **Typst**—a markup language built in Rust—to ensure extreme speed and efficiency when generating documentation for programming competitions.

### **Key Technical Features**

* **High-Performance Document Generation:** leveraged **Typst** for its real-time preview capabilities and significantly lower computational cost compared to LaTeX.
* **Multi-Language Support:** engineered a dynamic build system that generates specialized PDF dossiers for both **C++** and **Python 3** using a single source of truth.
* **Automated CI/CD Pipeline:** implemented **GitHub Actions** to automate the entire lifecycle: running stress tests for algorithms, compiling PDFs, and managing versioned releases.
* **Reliability through Stress Testing:** integrated a testing framework via **Makefile** to execute recursive stress tests in both Python and C++ before any release.
* **Developer-First Workflow:** optimized for VS Code integration using the Tinymist extension for live rendering and instant feedback during code editing.
