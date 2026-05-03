import re
import matplotlib.pyplot as plt

data = """# DISCREPANCY REPORT
# Compared first 50 sentences
# Total tokens compared : 481
# Total mismatches found: 109
# Sentences with errors : 44

# Format for each mismatch:
#   token   WRONG_TAG: output=<machine_tag> | gold=<reference_tag>


# Sentence 2: Global temperatures reached a record high last month .
high	WRONG_TAG: output=adj | gold=k2
month	WRONG_TAG: output=k2 | gold=k7

# Sentence 4: Scientists discovered a new species in the Western Ghats .
Ghats	WRONG_TAG: output=k2 | gold=k7

# Sentence 5: Space Exploration reaches a new milestone this week .
Exploration	WRONG_TAG: output=adj | gold=k1
reaches	WRONG_TAG: output=k1 | gold=V
milestone	WRONG_TAG: output=k1 | gold=k2
week	WRONG_TAG: output=k1 | gold=k7

# Sentence 6: The trade agreement aims to reduce export tariffs significantly .
agreement	WRONG_TAG: output=adj | gold=k1
aims	WRONG_TAG: output=k1 | gold=V
to	WRONG_TAG: output=- | gold=rt
reduce	WRONG_TAG: output=k4 | gold=V
tariffs	WRONG_TAG: output=k1 | gold=k2

# Sentence 7: Local communities are working to restore the ancient temple .
to	WRONG_TAG: output=- | gold=rt
restore	WRONG_TAG: output=k4 | gold=V

# Sentence 9: Oil prices stabilized after the recent production cut announcement .
recent	WRONG_TAG: output=k7 | gold=adj
production	WRONG_TAG: output=k2 | gold=adj
cut	WRONG_TAG: output=V | gold=adj

# Sentence 10: The university campus will host the national sports meet .
host	WRONG_TAG: output=k1 | gold=V
meet	WRONG_TAG: output=k1 | gold=k2

# Sentence 11: Renewable energy projects are expanding across the rural sector .
sector	WRONG_TAG: output=k2 | gold=k7

# Sentence 12: Global supply chains are recovering from recent disruptions .
supply	WRONG_TAG: output=adv | gold=adj
recent	WRONG_TAG: output=k5 | gold=adj

# Sentence 13: Urban planning must focus on sustainable public transport .
Urban	WRONG_TAG: output=k1 | gold=adj
planning	WRONG_TAG: output=V | gold=k1
focus	WRONG_TAG: output=k2 | gold=V

# Sentence 15: The tech startup secured funding for its innovative platform .
funding	WRONG_TAG: output=V | gold=k2
its	WRONG_TAG: output=k4 | gold=adj
platform	WRONG_TAG: output=k2 | gold=k4

# Sentence 16: Monsoon rains reached the southern coast earlier than expected .
earlier	WRONG_TAG: output=adj | gold=adv
than	WRONG_TAG: output=k2 | gold=-

# Sentence 17: Public health initiatives have reduced the spread of disease .
disease	WRONG_TAG: output=k2 | gold=r6

# Sentence 18: E-commerce growth continues to transform the retail landscape .
growth	WRONG_TAG: output=adj | gold=k1
continues	WRONG_TAG: output=k1 | gold=V
to	WRONG_TAG: output=- | gold=rt
transform	WRONG_TAG: output=k4 | gold=V
landscape	WRONG_TAG: output=k1 | gold=k2

# Sentence 19: High court judges emphasized the importance of digital privacy .
privacy	WRONG_TAG: output=k2 | gold=r6

# Sentence 20: Educational reforms are being implemented in several states .
states	WRONG_TAG: output=k2 | gold=k7

# Sentence 21: Manufacturing output increased for the third consecutive month .
Manufacturing	WRONG_TAG: output=V | gold=adj
output	WRONG_TAG: output=k2 | gold=k1
third	WRONG_TAG: output=k4 | gold=adj
month	WRONG_TAG: output=k2 | gold=k7

# Sentence 22: Archaeological survey found evidence of an ancient civilization .
civilization	WRONG_TAG: output=k2 | gold=r6

# Sentence 23: Wildlife conservation efforts have helped save endangered tigers .
save	WRONG_TAG: output=k2 | gold=V
endangered	WRONG_TAG: output=V | gold=adj

# Sentence 24: Airline industry expects a surge in summer holiday bookings .
industry	WRONG_TAG: output=adj | gold=k1
expects	WRONG_TAG: output=k1 | gold=V
surge	WRONG_TAG: output=k1 | gold=k2
bookings	WRONG_TAG: output=k1 | gold=rs

# Sentence 25: New legislation aims to protect the rights of workers .
legislation	WRONG_TAG: output=adj | gold=k1
aims	WRONG_TAG: output=k1 | gold=V
to	WRONG_TAG: output=- | gold=rt
protect	WRONG_TAG: output=k4 | gold=V
rights	WRONG_TAG: output=k1 | gold=k2
workers	WRONG_TAG: output=k2 | gold=r6

# Sentence 26: Remote work remains popular among several software development teams .
work	WRONG_TAG: output=adj | gold=k1
remains	WRONG_TAG: output=adj | gold=V
popular	WRONG_TAG: output=k1 | gold=adj
teams	WRONG_TAG: output=k1 | gold=k7

# Sentence 27: Interest rates might remain steady until the next quarter .
remain	WRONG_TAG: output=adj | gold=V
until	WRONG_TAG: output=k1 | gold=-
quarter	WRONG_TAG: output=adj | gold=k7

# Sentence 28: The library expanded its digital collection for remote access .
its	WRONG_TAG: output=k2 | gold=adj
remote	WRONG_TAG: output=k4 | gold=adj
access	WRONG_TAG: output=k2 | gold=k4

# Sentence 29: Sports fans celebrated the victory in the city center .
city	WRONG_TAG: output=k7 | gold=adj
center	WRONG_TAG: output=adj | gold=k7

# Sentence 30: Agriculture exports reached an all-time high this fiscal year .
all-time	WRONG_TAG: output=k2 | gold=adj
high	WRONG_TAG: output=adj | gold=k2
year	WRONG_TAG: output=k2 | gold=k7

# Sentence 31: Solar power plants are being installed in desert regions .
Solar	WRONG_TAG: output=k1 | gold=adj
desert	WRONG_TAG: output=k7 | gold=adj
regions	WRONG_TAG: output=k2 | gold=k7

# Sentence 32: Music festivals are returning after a two-year hiatus .
two-year	WRONG_TAG: output=k7 | gold=adj
hiatus	WRONG_TAG: output=k2 | gold=k7

# Sentence 33: Luxury car sales have seen a significant increase recently .
seen	WRONG_TAG: output=k1 | gold=V
increase	WRONG_TAG: output=k1 | gold=k2

# Sentence 35: Climate change is affecting the migration patterns of birds .
birds	WRONG_TAG: output=k2 | gold=r6

# Sentence 36: Inflation data suggests a cooling trend in the economy .
data	WRONG_TAG: output=adj | gold=k1
suggests	WRONG_TAG: output=k1 | gold=V
cooling	WRONG_TAG: output=V | gold=adj

# Sentence 37: Students participated in a large-scale tree planting drive .
large-scale	WRONG_TAG: output=k7 | gold=adj
tree	WRONG_TAG: output=k2 | gold=adj
planting	WRONG_TAG: output=V | gold=adj
drive	WRONG_TAG: output=adj | gold=k2

# Sentence 38: Digital banking has become the preferred choice for many .
banking	WRONG_TAG: output=V | gold=k1
become	WRONG_TAG: output=k2 | gold=V
preferred	WRONG_TAG: output=V | gold=adj

# Sentence 39: Regional tensions have impacted the local shipping routes .
shipping	WRONG_TAG: output=V | gold=adj

# Sentence 40: The literary festival hosted authors from across the world .
literary	WRONG_TAG: output=k1 | gold=adj
festival	WRONG_TAG: output=adj | gold=k1
world	WRONG_TAG: output=k7 | gold=k5

# Sentence 41: Space telescopes have captured images of distant galaxies .
galaxies	WRONG_TAG: output=k2 | gold=r6

# Sentence 42: Foreign direct investment reached a new peak this month .
month	WRONG_TAG: output=k2 | gold=k7

# Sentence 43: The metro rail project is expected to finish soon .
to	WRONG_TAG: output=- | gold=rt
finish	WRONG_TAG: output=k4 | gold=V
soon	WRONG_TAG: output=k2 | gold=adv

# Sentence 45: The pharmaceutical company received approval for its new vaccine .
approval	WRONG_TAG: output=adj | gold=k2
its	WRONG_TAG: output=k4 | gold=adj
vaccine	WRONG_TAG: output=k2 | gold=k4

# Sentence 46: Traditional crafts are being promoted through local cooperatives .
cooperatives	WRONG_TAG: output=k2 | gold=k3

# Sentence 47: Virtual reality is being used for advanced medical training .
advanced	WRONG_TAG: output=V | gold=adj
training	WRONG_TAG: output=V | gold=k4

# Sentence 48: Gold prices edged higher amid global economic uncertainty .
higher	WRONG_TAG: output=adj | gold=adv
amid	WRONG_TAG: output=k2 | gold=-
uncertainty	WRONG_TAG: output=k2 | gold=k7

# Sentence 49: The museum is hosting a special exhibit on coins .
coins	WRONG_TAG: output=k7 | gold=rs

# Sentence 50: New robotics technology is assisting in complex surgeries .
complex	WRONG_TAG: output=k7 | gold=adj
surgeries	WRONG_TAG: output=k2 | gold=r7"""

pattern = r"output=(.*?)\s+\|\s+gold=(.*)"
matches = re.findall(pattern, data)

error_counts = {}
for out, gold in matches:
    pair = f"Expected: {gold.strip()} \nMachine Predicted: {out.strip()}"
    error_counts[pair] = error_counts.get(pair, 0) + 1

sorted_errors = sorted(error_counts.items(), key=lambda item: item[1], reverse=True)[:10]

labels = [item[0] for item in sorted_errors][::-1]
counts = [item[1] for item in sorted_errors][::-1]

plt.figure(figsize=(10, 6))
bars = plt.barh(labels, counts, color='#4A90E2', edgecolor='black')
plt.title("Top 10 Most Frequent Tagging Errors", fontsize=14, pad=15)
plt.xlabel("Number of Occurrences", fontsize=12)
plt.ylabel("Tagging Mistake", fontsize=12)

for index, value in enumerate(counts):
    plt.text(value + 0.1, index, str(value), va='center', fontsize=11, fontweight='bold')

# Clean up axes
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig("tagging_errors_final.png", dpi=150)