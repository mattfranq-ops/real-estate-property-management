# Count of Ten

A turn-based boxing life sim in 2D pixel art. Every turn in the ring is one second. Outside the ring you plan your weeks around work, training, sleep, food and the people who keep you going. Hajime no Ippo and Ashita no Joe inspired the tone. The characters, gym and story are original.

Open `index.html` in a browser. It has no build step and no dependencies apart from two Google Fonts, and it saves to `localStorage`.

## The loop

1. **Create a boxer**: name, height, weight (sets the weight class), reach, stance, one of 5 styles, a background, and a look (skin, hair, trunks, gloves).
2. **Plan each week**: 7 days × (morning, afternoon, evening, night). There are presets, a grocery tier, and a live budget.
3. **Live the week**: activities change muscles, organs, skills, money, fatigue, sleep debt, nutrition, stress and relationships. Random scenes stop the week and ask you to choose.
4. **The break**: at the end of week 4 Pop gets the call for an undercard spot. Later fights are offered every few weeks. Dex Calloway, your rival, is fight #4.
5. **Weigh-in, then the fight**: damage carries back into the life sim as fractures, concussions and permanent brain loss.

## Body model

| System | Tracks | What it changes |
|---|---|---|
| Skeletal | skull, jaw, nose, orbitals, ribs, each hand, bone density | Chin, bleeding, breathing, gas recovery, hand power |
| Muscular | neck, shoulders, core, back, legs, arms | Power, chin (neck), liver tolerance (core) |
| Organs | brain (with a ceiling that drops after fights), heart, lungs, liver, kidneys | Gas tank, recovery, chin |
| State | fatigue, sleep debt, nutrition, stress, weight | Training gains, defense timing, reads, injury risk |

Neglect has a cost. Short sleep slows your hands and weakens your reads. Eating instant noodles burns muscle and bone. Overtraining and dock shifts cause injuries. Sparring slowly takes away brain health you can't get back.

## The second-by-second fight

- Both fighters commit an action for the same second. The AI picks its action before you do.
- **Hitboxes are tested per point.** Each punch has an impact shape in the defender's frame, for example a hook is a horizontal band and an uppercut is a vertical column. Each defensive action moves the head and torso hitboxes and places glove and forearm rects. If the head moved out of the shape, the punch misses. If gloves cover too much of it, it's blocked. Otherwise the region with the most clean contact (chin, jaw, temple, eye, nose, liver, solar plexus, ribs…) takes the damage.
- This makes the counters work out from the geometry instead of from a lookup table. A slip beats a straight but moves your head into the lead hook. A duck beats hooks and overhands but drops you onto an uppercut. A high guard stops head shots and leaves the liver open. A feint freezes a defender for a second. A punch drops that hand's guard, so jabbing opens you to the overhand.
- **Range** (inside, mid, long) controls which punches reach. The **clinch** smothers straights. **Speed** settles trades.
- **Reads**: each second you get a tell. How accurate it is depends on ring IQ, eye swelling, damage and sleep. Feints show up as false tells.
- **The AI learns your habits** (n-gram model of your actions) and scores its options by running your likely replies through the same hitbox engine.
- **Combos** are written in a notebook and play one step per second. You can break off a combo at any second.
- **Knockdowns** come from head shock passing your chin, flash counters, a delayed liver shot, or exhaustion. During the count you reach for a memory (Mina, Rosa, Pop, Dex, your father's gloves). The strength of that bond sets your chance to get up. Each memory works once per fight.
- **Resolve** builds as you take punishment. At 100 you go *Past the Limit* for 8 seconds.
- Between rounds, Pop reads the opponent's habits and you choose one corner treatment. Three judges score 10-point must with different biases.

## Tuning knobs

- Round length: 30 / 60 / 180 s (button in the planner)
- `TECH`: punch power, speed, cost, ranges
- `SHAPES`, `GUARDS`, `REG_*`: hitbox geometry
- `REGFX`: what each region does to the body
- `ACT`, `EVENTS`, `OPPS`: life-sim activities, scenes, opponents
