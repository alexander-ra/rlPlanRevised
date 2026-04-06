import re

with open("/home/alexanderandreev/rlProjects/rlPlanRevised/deliverables/reports/step01/report.md", "r") as f:
    text = f.read()
    
# Add an explicit explanation about the SB3 defaults being tuned for Atari
if "tuned for robustness across many environments" in text:
    text = text.replace("tuned for robustness across many environments, not for a single task.",
                       "tuned for robustness across many environments (such as Atari games with millions of steps and discrete image inputs), not for classic control tasks like CartPole. This causes the SB3 default algorithm to struggle or fail without extensive tuning compared to our environment-specific hyperparameters.")
    
with open("/home/alexanderandreev/rlProjects/rlPlanRevised/deliverables/reports/step01/report.md", "w") as f:
    f.write(text)

with open("/home/alexanderandreev/rlProjects/rlPlanRevised/deliverables/reports/step01/summary/summaryEn.md", "r") as f:
    stext = f.read()

if "SB3's defaults are designed for robustness across diverse environments;" in stext:
    stext = stext.replace("SB3's defaults are designed for robustness across diverse environments;",
                          "SB3's defaults are designed for robust performance across diverse, long-training domains like Atari games — not brief episode classic control environments like CartPole;")
    
with open("/home/alexanderandreev/rlProjects/rlPlanRevised/deliverables/reports/step01/summary/summaryEn.md", "w") as f:
    f.write(stext)
print("Updated English files with explicit SB3 causes.")
