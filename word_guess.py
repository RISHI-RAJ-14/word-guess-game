import random
import streamlit as st

# Word banks with simpler words
word_banks = {
    "Programming": ["python", "developer", "programming", "algorithm", "function", 
                   "variable", "debugging", "compiler", "codechef", "machine"],
    "OS": ["kernel", "process", "thread", "scheduling", "deadlock", 
          "memory", "filesystem", "interrupt", "paging", "semaphore"],
    "DBMS": ["database", "query", "transaction", "normalization", "index", 
            "join", "schema", "trigger", "view", "constraint"],
    "OOPS": ["object", "class", "inheritance", "polymorphism", "encapsulation", 
            "abstraction", "interface", "constructor", "overloading", "composition"],
    "CN": ["protocol", "router", "packet", "firewall", "bandwidth", 
          "topology", "ethernet", "ipaddress", "dns", "tcp"]
}

def scramble_word(word):
    """Scramble the letters of a word randomly"""
    if len(word) <= 1:
        return word
    word_list = list(word)
    while True:
        random.shuffle(word_list)
        scrambled = ''.join(word_list)
        if scrambled != word:  # Ensure scrambled is different from original
            return scrambled

def play_game():
    st.title("🎯 Word Scramble Game")
    st.write("Select a subject and unscramble the word!")

    # Subject selection
    subject = st.selectbox("Choose a subject:", list(word_banks.keys()), key="subject_select")
    
    # Initialize/reset game when subject changes
    if 'current_subject' not in st.session_state or st.session_state.current_subject != subject:
        st.session_state.current_subject = subject
        reset_game(subject)

    # Display scrambled word
    st.subheader(f"Subject: {subject}")
    st.markdown(f"**Scrambled word:** `{st.session_state.scrambled_word}`")

    # Guess input (disabled if game over)
    guess = st.text_input("Your guess:", 
                         value="", 
                         disabled=st.session_state.game_over).lower().strip()
    
    # Game controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Guess", disabled=st.session_state.game_over):
            handle_guess(guess, subject)
    with col2:
        if st.button("New Word"):
            reset_game(subject)
            st.rerun()

    # Display attempts and messages
    if st.session_state.attempts > 0:
        st.write(f"Attempts used: {st.session_state.attempts}/3")
    
    if st.session_state.message:
        if "Correct" in st.session_state.message:
            st.success(st.session_state.message)
            # Show "Start New Game" button after winning
            if st.button("🎮 Start New Game"):
                reset_game(subject)
                st.rerun()
        else:
            st.error(st.session_state.message)

def reset_game(subject):
    """Reset the game state with a new word"""
    st.session_state.original_word = random.choice(word_banks[subject])
    st.session_state.scrambled_word = scramble_word(st.session_state.original_word)
    st.session_state.attempts = 0
    st.session_state.message = ""
    st.session_state.game_over = False

def handle_guess(guess, subject):
    """Process user's guess"""
    if st.session_state.game_over:
        return
        
    if not guess:
        st.session_state.message = "Please enter a guess"
        return
        
    st.session_state.attempts += 1
    
    if guess == st.session_state.original_word:
        st.session_state.message = "🎉 Correct! You won! 🎉"
        st.session_state.game_over = True
        st.balloons()
    else:
        if st.session_state.attempts >= 3:
            st.session_state.message = f"Game over! The word was: {st.session_state.original_word}"
            st.session_state.game_over = True
        else:
            st.session_state.message = "Wrong guess. Try again!"

if __name__ == "__main__":
    play_game()