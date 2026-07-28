# Human markers: the additive pass

Removing tells makes text neutral. Neutral is not human. This file is the other half of the job: what to put back, with worked examples.

Read this whenever a rewrite comes out technically clean but flat. That flatness is the most common failure mode of aggressive editing, and it is a worse outcome than the original, because uniformity is the underlying tell that all the surface patterns are symptoms of.

**Contents**
- [Rhythm](#rhythm)
- [Specificity](#specificity)
- [Hedges and commitment](#hedges-and-commitment)
- [Plain language](#plain-language)
- [Voice](#voice)
- [Deliberate imperfection](#deliberate-imperfection)
- [Full before and after](#full-before-and-after)

---

## Rhythm

Model prose clusters between 15 and 25 words per sentence with low variance. Human prose swings wildly. This is the single strongest statistical separator and the one that survives every vocabulary edit, so treat a flat variance number as a real defect rather than a stylistic preference.

**Targets:** in every ten sentences, at least one under eight words and at least one over twenty-five. Paragraphs between one and six sentences. A one-sentence paragraph is a distinctly human move.

**Before** (every sentence 18-22 words, variance near zero):

> The platform integrates with existing enterprise systems to streamline workflow management across departments. Teams can access shared dashboards that provide visibility into project status and resource allocation. Administrators configure permissions at a granular level to maintain security while enabling collaboration.

**After:**

> The platform plugs into whatever you already run. Teams get one dashboard showing project status and who is on what, which sounds obvious until you have watched three departments each maintain their own spreadsheet version of the same information and then argue about which one is current. Admins set permissions per person. That part is boring but it is the part IT asks about first.

Sentence lengths went from 18/20/19 to 8/47/5/13. Same information, different shape.

---

## Specificity

One concrete anchor per paragraph: a number, a name, a date, a place, a product, a real example. This is the direct antidote to regression toward the mean, because a specific fact is by definition statistically unlikely.

| Generic | Specific |
|---|---|
| a leading cloud provider | AWS |
| studies show significant improvement | the 2024 Stanford trial cut it by 31% |
| in recent years | since roughly 2022 |
| a major setback | we lost the Tata pilot in week three |
| substantial growth | 40 to 310 users in five months |

**Never invent a specific to satisfy this rule.** If the draft has no real detail available, that is a research gap rather than a style problem. Flag it and ask the writer for the number. An invented statistic is a far worse failure than a generic sentence, and fabricated specificity is itself one of the things this skill exists to catch.

---

## Hedges and commitment

Models are trained toward confident flatness. They avoid both ends: they will not hedge, and they will not commit hard. Humans do both, often in the same paragraph.

**Hedges to add back:** probably, roughly, tends to, in most cases, I think, my guess is, something like, more or less, at least in our experience.

**Commitments to add back:** the only, the first, the worst, one of the best, nobody does this, this is wrong.

> **Before:** The approach offers several potential advantages for organizations seeking to optimize their deployment processes.
>
> **After:** This is probably the only setup that survives a bad Friday deploy. Probably. We have broken it twice.

The hedge and the hard claim reinforce each other. Confidence with visible uncertainty around it reads as someone who has actually done the thing.

---

## Plain language

Put back what the model edited out.

**Copulas.** "is", "are", "has", "there is", "it was". If the draft says "serves as", "stands as", "functions as", "represents", "boasts", "features", or "offers", check whether a copula was avoided and restore it.

> Gallery 825 serves as the association's exhibition space for contemporary art. The gallery features four separate rooms.
>
> → Gallery 825 is the association's exhibition space for contemporary art. There are four rooms.

**Plain verbs.** wrote not authored, used not utilized, moved not relocated, tried not attempted, bought not acquired, helped not facilitated, started not embarked upon, showed not demonstrated, has not possesses.

**Mild wordiness.** Leave one or two of these per page: "in order to", "the fact that", "a part of", "as a result of", "all of the". Do not hunt them down and do not add them mechanically either. The point is that ruthless compression is a machine signature, so the absence of every last redundancy is itself suspicious.

---

## Voice

One opinionated or first-person sentence per section, wherever the format allows it. Models produce views from nowhere. A person writing has a position, a history with the subject, and things they find annoying.

Ways to get voice in without changing the facts:
- Say which part you found hardest or most surprising
- Name what you tried that did not work
- Disagree with the conventional take, briefly
- Admit what you do not know
- Address the reader directly about something specific to them

> **Before:** Implementation typically requires two to three weeks depending on organizational complexity.
>
> **After:** Budget three weeks. Every vendor says two, we said two, and it was three.

---

## Deliberate imperfection

Uniform polish is the giveaway. Some texture worth allowing:

- A parenthetical aside that is not strictly necessary
- A sentence that starts with And, But, or So
- A digression that returns to the point
- A slightly odd word choice, as long as it is the right word
- An unresolved thought, flagged as unresolved

None of this means writing badly. It means writing like someone who was thinking while writing rather than assembling from a template.

---

## Full before and after

**Before, 96 words, scores about 35:**

> Founded in 2019, TechFlow has emerged as a pivotal player in the workflow automation landscape, serving as a testament to the growing demand for intelligent business solutions. The company boasts a comprehensive suite of tools that range from task management to advanced analytics, empowering organizations to streamline operations. Industry experts have noted that TechFlow's approach represents a significant shift in how enterprises think about automation. Despite its rapid growth, the company faces challenges in a competitive market. Nevertheless, TechFlow remains well-positioned to capitalize on emerging opportunities, underscoring its commitment to innovation.

Tells present: puffery (pivotal, testament, significant shift, underscoring, commitment to), copula avoidance (has emerged as, serving as, boasts), false range (from task management to advanced analytics), weasel attribution (industry experts have noted), the Despite-its-growth-faces-challenges formula, a closing summary that says nothing, and zero specifics across 96 words.

**After, 91 words, scores about 90:**

> TechFlow started in 2019 selling workflow automation to mid-market companies. The product is task management with an analytics layer bolted on, which is a less exciting description than the one on their homepage but a more accurate one. It works. Their pitch is that most automation tools assume you already know what to automate, and theirs does not, which is either a real insight or good marketing depending on who you ask. Growth has been fast. Retention is the open question, and they have not published a number.

Almost the same length. Every claim is now either concrete or explicitly marked as uncertain, the sentence lengths run 13/33/2/38/3/16, and there is a person behind it with an opinion.

Note what happened to the last sentence. The original ended with reassurance. The rewrite ends with an unanswered question, because that is what the writer actually knows.

---

## Numbers to aim for

The scanner reports these. They are the targets that survive every vocabulary edit, because they describe shape rather than word choice.

| Metric | Machine typical | Human typical |
|---|---|---|
| Sentence length stdev | under 8 | 12 to 20 |
| Copulas per 100 words | under 3 | 5 to 8 |
| Hedges per 200 words | 0 | 2 to 4 |
| Shortest sentence | 12+ words | under 8 words |
| Concrete specifics | 0 to 1 per 200 words | 2+ per 200 words |

The copula rate is the most robust of these. One study measured a drop of more than 10% in the words "is" and "are" across academic writing in 2023, with no prior trend, and found that models removed them even when asked only to "revise the following sentence". A draft can pass every other check and still give itself away on this one number.

Do not game these mechanically. Padding a text with "is" and stray hedges to hit a target produces something that reads as broken rather than human. Fix the sentences properly and the numbers follow.
