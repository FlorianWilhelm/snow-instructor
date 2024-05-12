"""All settings for the Snow Instructor project."""

SNOWDOCS_TABLE = 'SNOWDOCS'
SNOWINSTRUCTOR_WH = 'SNOWINSTRUCTOR_WH'  # same as in snowflake.yml!
SNOWINSTRUCTOR_DB = 'SNOWINSTRUCTOR'  # same as in ~/.snowflake/connections.toml

QUIZ_PROMPT = (
    'Based on the following excerpt from the Snowflake documentation, generate a multiple-choice question '
    'that tests understanding of the key concept discussed. Include four answer choices and indicate the '
    'correct answer.\n{text}'
)

START_COMMENTS = [
    "Welcome, everyone! I hope you brought your brains today. You'll need them.",
    "Alright, let's get this disaster—uh, I mean, game—started!",
    "Here we go! Remember, it's not about winning, but let's be honest, yes it is.",
    "Gather round, everyone. It's time to find out who's really been paying attention in life.",
    "Let the games begin! May the odds be ever in your favor. Because you'll need it.",
    "Welcome to the game where everyone's made up and the points don't matter!",
    "Let's start the game. Remember, it's just like school, but fun... I hope.",
    "Let's get ready to rumble! And by rumble, I mean fumble through these questions.",
    'Welcome to what will undoubtedly be the highlight of your day.',
    "Fasten your seatbelts, it's going to be a bumpy night!",
    "Let's kick this off! I hope you've all lowered your expectations.",
    "And we're off! Don't worry, it only feels like it's going to last forever.",
    'Ready, set, go! May the least clueless person win!',
    "Welcome to our game show, where you'll laugh, you'll cry, and you'll wish you'd stayed home.",
    "Let the battle of wits begin! Spoiler: it won't be a long battle.",
    "Alright, everyone, try to contain your excitement. Or don't. Up to you.",
    "Welcome to the least serious competition you'll ever be a part of.",
    "Here we go! I promise it's not as complicated as it seems. It's more.",
    "Let's dive in, and may your guesses be more than wild stabs in the dark!",
    "Welcome! Let's find out who's going to be accidentally brilliant today.",
    "I hope you're all ready to play 'Guess What the Game Master's Thinking.'",
    "Let's start the game! Or as I like to call it, 'Who needs Google?'",
    "Game faces on, everyone! Not that it will help much, but it's cute you'll try.",
    "Let's start this journey into the unknown, slightly embarrassing, and downright puzzling!",
    "Welcome to our game, where you'll find out who your real friends are.",
    "Shall we start the quiz? I'm sure you're all eager to demonstrate your vast knowledge about very little.",
    "Here we go—let's see which of you can claim the title of 'Least Uninformed.'",
    "Welcome! Try not to look so nervous; it's hardly ever fatal.",
    "Let the games begin! Just a reminder, there's no crying in trivia.",
    "Alright, let's get this over with—I mean, let's have some fun!",
    "And we begin! Remember, it's not whether you win or lose, it's how you blame the game.",
    "Let's get started, shall we? I can feel the excitement, or something like that.",
    'Welcome to what I promise will be a mildly amusing few hours.',
    "Let's kick this off! I'd say 'may the best man win', but let's face it, it's anyone's game.",
    "Here we go, the moment you've all been waiting for—or dreading.",
    "Welcome to the game! Spoiler alert: it's harder than it looks.",
    "Ready or not, here we go! Let's uncover some fun facts and embarrassing guesses.",
    "Welcome! It's time to prove your mettle, or at least your ability to remember useless trivia.",
    "Here we go! Keep your wits about you and your smartphones away—you're on the honor system!",
    "Let's begin! Don't worry, the questions aren't too hard. I think.",
    'Welcome players! Get ready for a ride on the trivia roller coaster—ups, downs, and occasional nausea included.',
    "Let's get rolling! Hopefully, your brain's in gear, because we're not stopping for stragglers.",
    "Alright, let's launch this circus! And no, that's not a clue for the first question.",
    'Welcome to the show that tests your knowledge and occasionally your patience.',
    "Here we start! Let's see who's a trivia champion and who's just good at smiling.",
    "Welcome! Let's set the intellectual bar low, and limbo our way through!",
    'Welcome to the game where everyone ends up questioning their life choices that led them here.',
    "Okay, let's get this quiz on the road! Not literally, that would be a safety hazard.",
    "Let's begin the mayhem! And remember, it's all in good fun... mostly.",
    'Alright, time to start the game that separates the know-it-alls from the know-nothings.',
]

CORRECT_COMMENTS = [
    'Right? Yes. Expected? Absolutely not.',
    'Even a broken clock is right twice a day!',
    'Wow, you actually got it. Alert the media!',
    'Did someone whisper the answer to you?',
    "Correct... Are you sure you're feeling okay?",
    "Someone's been studying! Or was it a lucky guess?",
    'Look at you, being all smart and stuff.',
    'Congratulations! Even a squirrel finds a nut once in a while.',
    "Correct! This won't get any easier, just so you know.",
    "Right answer! Did you Google that when I wasn't looking?",
    'Yes, but can you do it again?',
    'Well, color me impressed... and slightly suspicious.',
    'Finally, something you knew!',
    'Whoa, a correct answer! I need to sit down.',
    "Spot on! Don't get used to this feeling.",
    "Correct! You're full of surprises.",
    'Oh, I see the internet is working fine today.',
    "You got it! But don't let it go to your head.",
    'Correct! Are the planets aligned or something?',
    "I'd pat you on the back, but let's not make this a habit.",
    'You got it right! Was that your first guess?',
    "Hey, no one's more surprised than me that you got that right.",
    "Correct, but let's not make a big deal out of it.",
    'Right? Yes. Miracles do happen!',
    "Congratulations, you're not as wrong as usual today!",
    'Correct. Did you eat a smart breakfast this morning?',
    'Correct! Did you hack into my notes?',
    'Look at that, right for once!',
    'Finally, the stars aligned for you.',
    'Wow, correct! What are the odds?',
    "Yes, that's right. I'm as shocked as you are.",
    'Correct! Quick, someone mark the calendar.',
    "Bingo! Are you sure you're playing fair?",
    'Right answer! Who helped you?',
    'Correct! Is today opposite day?',
    "Yes, and I'm genuinely shocked.",
    'Huh, you got it. I was not prepared for that.',
    'Spot on! Did you peek?',
    "You're right! Now, don't let it get to your head.",
    "Correct! That's... actually amazing.",
    "Well, a correct answer! That's a rare sight.",
    'You nailed it! Was that a wild guess?',
    "That's right! Celebrate this moment.",
    'Correct! How long have you been holding onto that fact?',
    'Yes, finally! Was that as hard for you as it seemed?',
    "Correct! Someone's been doing their homework.",
    'Right! How did that happen?',
    'Correct! Did you do a victory dance yet?',
    'Yes, you got it. Should we throw a party now?',
    "You're right! Someone give this person a cookie!",
]

INCORRECT_COMMENTS = [
    "Well, at least you're consistent...ly wrong.",
    'Was that your final answer or just a practice run?',
    'Right answer... for a different question!',
    'Even a stopped clock is right twice a day, but you? Not so much.',
    "Ah, boldly wrong! There's merit in commitment, I suppose.",
    'You really went out on a limb there, huh? Too bad it was the wrong tree.',
    'Congratulations! That was a one-of-a-kind answer. Seriously, no one else would choose that.',
    "Oops! Wrong answer, but don't worry—nobody's keeping score. Just kidding, we all are.",
    'Was that the answer you meant to give, or just the first one that came to mind?',
    "You're really exploring all the possibilities, aren't you? All the wrong ones, that is.",
    'A swing and a miss! Maybe we should switch to an easier game?',
    "Are you sure you don't want to phone a friend? Or maybe all of them?",
    "If this were golf, you'd be winning with all those attempts away from the target.",
    "You've got a talent for the unexpected. Mainly, unexpectedly wrong answers.",
    "It's a good thing curiosity doesn't actually kill cats, or we'd be in trouble with that answer.",
    'Well, points for creativity, if not for accuracy!',
    'That answer was out in left field. The left field of a different ballpark.',
    'I appreciate your commitment to the wrong answers. Very dedicated.',
    'Oh, close! But in the same way that the moon is close to the sun.',
    "That answer was so original, it's almost like it wasn't meant for this game.",
    "Clearly, you're a trailblazer... in the wrong direction.",
    "Are we playing the same game? Because that answer wasn't even close!",
    'That was a fantastic answer... for a completely different question.',
    'Keep this up and you might just invent a new way to be wrong.',
    "Historically unique! There's never been a wrong answer quite like that before.",
    "And here I was thinking today couldn't get any more surprising.",
    'Your answer is so out there, it might just need a passport.',
    "That's an interesting approach... to losing.",
    "If wrong answers were treasure, you'd be a billionaire.",
    'Wow, with answers like that, who needs correct ones?',
    "You might not be right, but you're definitely wrong with style!",
    "That's an impressive stretch. Gymnastics next?",
    "Oh, bold choice! Let's see how it doesn't pay off.",
    "Is this your strategy? Because it's... something.",
    "I didn't know we were giving points for creativity today.",
    "You're so far off, you might need a map to get back.",
    'Your answer just left the chat.',
    'Is there a prize for the most original wrong answer? Asking for a friend.',
    'You could start a blog with all these unique perspectives.',
    "If we were looking for the least likely answer, you'd have just won.",
    'That answer was like a plot twist in the wrong book.',
    'With guesses like that, who needs certainty?',
    "You're rewriting the rules of wrong answers, one guess at a time.",
    "If creativity scored points, you'd be the champ.",
    "It's not just wrong, it's advanced wrong.",
    'A for effort, F for accuracy.',
    "Let's chalk that one up to artistic license.",
    "You're not just thinking outside the box; you left the box behind.",
    'That was a leap of faith... off a cliff.',
    'Are you pioneering new ways to be wrong? Because bravo!',
]


GREETINGS = [
    'Ah, fresh meat! Welcome to the chaos.',
    "Look who finally showed up! We've been expecting you... sort of.",
    'Here comes a new challenger! Or just another casualty, time will tell.',
    'Welcome! We were running out of people to beat.',
    'Ah, a new victim—I mean, player! Welcome aboard!',
    "Welcome! Don't worry, we only bite if you win.",
    "New face, huh? Let's see how long the enthusiasm lasts.",
    'Oh, joy! Another player who thinks they can win. Cute.',
    'Greetings, newcomer. Prepare for your inevitable defeat!',
    'Welcome! Just remember, the first rule is there are no rules. (Just kidding, there are lots of rules.)',
    'Ah, welcome! You look just like the last person who lost spectacularly.',
    "You're new here, right? Don't worry, the confusion is normal.",
    "Welcome to the jungle! We've got fun and games. And yes, a little bit of chaos.",
    'Enter the newcomer! May your wit be as sharp as your looks.',
    'Hello and welcome! May your stay here be both puzzling and enlightening.',
    'Ah, our latest adventurer! Brace yourself; it gets weird here.',
    'Welcome! Try to look smarter than you are—it helps.',
    'Greetings! If you need any help, just ask someone else.',
    "Welcome to the fold. It's too late to escape now.",
    "Hello! If you came looking for a gentle introduction... you won't find it here.",
    "A new challenger has appeared! We'll try to go easy on you. Try.",
    "Greetings, newbie! Spoiler alert: we're all mad here.",
    "Welcome, welcome! You'll either leave as a hero or one of us.",
    'A warm welcome to you! Or at least as warm as we get around here.',
    'Hey there! You look just as confused as we felt when we started.',
    'Welcome! We were just saying we needed a new player to liven up the losses.',
    'Look what the cat dragged in! Hopefully, you play better than you look.',
    'Welcome to the game where your guess is as good as mine. Literally.',
    "Oh, a new player! Are you sure you're ready for this?",
    "Welcome aboard! We hope you're better at this than your predecessors.",
    'New player alert! The odds just got more interesting.',
    "Hey, welcome! You don't look totally hopeless.",
    'Greetings, Earthling. Ready to conquer or be conquered?',
    "Welcome! It's all downhill from here, so enjoy the view!",
    "Hello to our newest player! Don't mind the chaos; it's part of the charm.",
    "Welcome! Let's find out if you're as good as you think you are.",
    "Ah, a newcomer. Don't worry, it only seems impossible.",
    'Hey there! Ready to lose? Just kidding... sort of.',
    'Welcome! Just in time to watch your hopes get dashed. Fun, right?',
    "New here? Don't worry, the despair grows on you.",
    "Ah, a new face! Spoiler: the game's rigged. (Just kidding... maybe.)",
    'Greetings! Ready to embark on a journey of questionable decisions?',
    'Welcome, new player! May your answers be correct and your losses be spectacular.',
    "Hello! Keep your expectations low, and you'll do fine.",
    "A newbie! Let's see if you're a quick learner or just quick to lose.",
    "Welcome! We'll start easy on you. Or maybe we won't.",
    "Hey, new player! Strap in; it's going to be a bumpy ride.",
    'Hello, fresh talent! Ready to be thoroughly bamboozled?',
    'Welcome! We needed someone else to help balance out the average score.',
    "Welcome! Remember, it's not about winning, but who you beat.",
]
