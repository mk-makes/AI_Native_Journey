import React, { useState, useEffect, useCallback } from 'react';

// Card component for individual game cards
const Card = ({ card, onClick, flippedCardsIds, matchedCardsIds }) => {
  // Determine if the card is currently flipped (either temporarily or permanently matched)
  const isFlipped = flippedCardsIds.includes(card.id) || matchedCardsIds.includes(card.id);
  // Determine if the card is permanently matched
  const isMatched = matchedCardsIds.includes(card.id);

  return (
    <div
      className={`
        relative flex items-center justify-center p-4 md:p-6 h-32 md:h-40 rounded-xl cursor-pointer
        transform transition-all duration-300 ease-in-out select-none backface-hidden
        ${isMatched ? 'bg-green-500 bg-opacity-70 scale-105 shadow-inner pointer-events-none' :
           isFlipped ? 'bg-blue-600 shadow-lg rotate-y-180' :
           'bg-indigo-700 hover:bg-indigo-600 shadow-md hover:shadow-xl'}
      `}
      // Only allow clicking if the card is not matched and not currently flipped (unless it's the second card being flipped)
      onClick={() => onClick(card)}
      style={{ transformStyle: 'preserve-3d' }}
    >
      {/* Card Front (Content) */}
      <div className={`absolute w-full h-full flex items-center justify-center text-center p-2
        ${isFlipped ? 'opacity-100' : 'opacity-0'}`}
        style={{ transform: 'rotateY(0deg)' }}
      >
        <span className="text-sm sm:text-base md:text-lg font-semibold leading-tight">
          {card.content}
        </span>
      </div>

      {/* Card Back (Question Mark) */}
      <div className={`absolute w-full h-full flex items-center justify-center text-5xl md:text-6xl font-extrabold
        ${isFlipped ? 'opacity-0 rotate-y-180' : 'opacity-100'}`}
        style={{ transform: 'rotateY(180deg)' }}
      >
        ?
      </div>
    </div>
  );
};

// Main App component for the variable matching game
function App() {
  // Define the initial set of Python variable pairs (variable concept and its description)
  const initialConcepts = [
    { name: 'Python String', description: '`name = "Alice"` (text)' },
    { name: 'Python Integer', description: '`age = 30` (whole number)' },
    { name: 'Python Float', description: '`price = 19.99` (decimal number)' },
    { name: 'Python Boolean', description: '`is_active = True` (True/False)' },
    { name: 'Python List', description: '`items = [1, 2, 3]` (ordered collection)' },
    { name: 'Python Dictionary', description: '`person = {"age": 30}` (key-value pairs)' },
    { name: 'Python None', description: '`data = None` (absence of a value)' },
    { name: 'Python Tuple', description: '`coords = (10, 20)` (immutable sequence)' },
  ];

  // Function to shuffle an array (Fisher-Yates algorithm)
  // Wrapped in useCallback to ensure it's stable and doesn't cause unnecessary re-renders
  const shuffleArray = useCallback((array) => {
    let currentIndex = array.length, randomIndex;
    while (currentIndex !== 0) {
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;
      [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
    }
    return array;
  }, []); // Empty dependency array means this function is created once and memoized.

  // State to hold the current cards on the board.
  // Initialized using a function for lazy initialization to ensure it only runs once.
  const [cards, setCards] = useState(() => {
    const gameCards = [];
    initialConcepts.forEach((concept, index) => {
      // Create a card for the concept name
      gameCards.push({
        id: `name_${index}`,
        conceptId: index, // Link both parts of the pair
        content: concept.name,
        type: 'name'
      });
      // Create a card for the concept description
      gameCards.push({
        id: `desc_${index}`,
        conceptId: index, // Link both parts of the pair
        content: concept.description,
        type: 'description'
      });
    });
    return shuffleArray(gameCards); // Shuffle and return the initial cards
  });

  // State to keep track of cards that are currently flipped by the user
  const [flippedCards, setFlippedCards] = useState([]); // Stores card objects
  // State to keep track of card IDs that have been successfully matched
  const [matchedCards, setMatchedCards] = useState([]); // Stores card IDs
  // State for the number of moves made by the player
  const [moves, setMoves] = useState(0);
  // State to indicate if the game is over
  const [gameOver, setGameOver] = useState(false);
  // State to prevent rapid clicking while cards are being compared/flipped back
  const [canClick, setCanClick] = useState(true);
  // State for the timer: 3 minutes = 180 seconds
  const [timeLeft, setTimeLeft] = useState(180);
  // State to track if the game has started (first click) to begin the timer
  const [gameStarted, setGameStarted] = useState(false);

  // Function to reset the game state. This will be called by the "Play Again" button.
  const resetGame = useCallback(() => {
    const gameCards = [];
    initialConcepts.forEach((concept, index) => {
      gameCards.push({
        id: `name_${index}`,
        conceptId: index,
        content: concept.name,
        type: 'name'
      });
      gameCards.push({
        id: `desc_${index}`,
        conceptId: index,
        content: concept.description,
        type: 'description'
      });
    });
    setCards(shuffleArray(gameCards));
    setFlippedCards([]);
    setMatchedCards([]);
    setMoves(0);
    setGameOver(false);
    setTimeLeft(180); // Reset timer
    setGameStarted(false); // Reset game started flag
    setCanClick(true);
  }, [initialConcepts, shuffleArray]); // Dependencies for resetGame are stable

  // Effect to manage the game timer
  useEffect(() => {
    let timer;
    // Start timer only if game has started and is not over and time is left
    if (gameStarted && !gameOver && timeLeft > 0) {
      timer = setInterval(() => {
        setTimeLeft(prevTime => prevTime - 1);
      }, 1000);
    } else if (timeLeft === 0 && gameStarted && !gameOver) {
      // If time runs out and game is not yet won
      setGameOver(true); // Indicate game over due to time
    }

    // Cleanup function to clear the interval when the component unmounts or dependencies change
    return () => clearInterval(timer);
  }, [gameStarted, gameOver, timeLeft]); // Dependencies: timer depends on gameStarted, gameOver, and timeLeft

  // Effect to check for matches when two cards are flipped
  useEffect(() => {
    if (flippedCards.length === 2) {
      setCanClick(false); // Disable clicking while checking
      const [firstCard, secondCard] = flippedCards;

      // Match if they share the same conceptId and are of different types (name vs. description)
      const isMatch = firstCard.conceptId === secondCard.conceptId &&
                      firstCard.type !== secondCard.type;

      if (isMatch) {
        setMatchedCards(prev => [...prev, firstCard.id, secondCard.id]);
        // Delay clearing flippedCards slightly to avoid immediate re-triggering loop
        setTimeout(() => {
          setFlippedCards([]); // Clear flipped cards
          setCanClick(true); // Re-enable clicking
        }, 0); // Execute immediately after current task
      } else {
        const timer = setTimeout(() => {
          setFlippedCards([]); // Clear flipped cards (visually flips them back)
          setCanClick(true); // Re-enable clicking
        }, 1000);
        return () => clearTimeout(timer); // Cleanup function: clear timeout if component unmounts or effect re-runs
      }
    }
  }, [flippedCards]); // Only depends on flippedCards; state updates are now safely deferred

  // Effect to check if the game is over (all cards matched)
  useEffect(() => {
    if (matchedCards.length > 0 && matchedCards.length === cards.length && cards.length > 0) {
      setGameOver(true);
      setGameStarted(false); // Stop the timer when game is won
    }
  }, [matchedCards, cards.length]); // Depends on matchedCards and the total number of cards

  // Handler for when a card is clicked
  const handleCardClick = (clickedCard) => {
    // Start the game timer on the first valid click
    if (!gameStarted && !gameOver) {
      setGameStarted(true);
    }

    // Ignore clicks if not clickable (e.g., during comparison delay),
    // or if the card is already matched, or if it's already one of the two currently flipped cards.
    if (!canClick || matchedCards.includes(clickedCard.id) || flippedCards.some(fc => fc.id === clickedCard.id)) {
      return;
    }

    // Increment moves for every valid click
    setMoves(prevMoves => prevMoves + 1);

    // Only allow flipping up to two cards at a time
    if (flippedCards.length < 2) {
      // Add the newly flipped card to the flippedCards state
      setFlippedCards(prev => [...prev, clickedCard]);
    }
  };

  // Format time for display
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-800 to-indigo-900 text-white flex flex-col items-center justify-center p-4 font-sans">
      {/* Header and Title */}
      <h1 className="text-4xl md:text-5xl font-extrabold mb-6 text-center drop-shadow-lg animate-fade-in">
        Python Variable Match
      </h1>
      <p className="text-xl md:text-2xl mb-8 text-center max-w-2xl opacity-90">
        Match Python variable concepts with their examples!
      </p>

      {/* Game Stats and Timer */}
      <div className="flex flex-col sm:flex-row justify-between items-center w-full max-w-md mx-auto mb-6 text-lg font-semibold bg-white bg-opacity-20 rounded-lg p-4 shadow-xl">
        <span className="flex items-center mb-2 sm:mb-0">
          {/* SVG icon for moves */}
          <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          Moves: {moves}
        </span>
        <span className="flex items-center mb-2 sm:mb-0">
          {/* SVG icon for matched pairs */}
          <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          Matched: {matchedCards.length / 2} / {initialConcepts.length}
        </span>
        <span className={`flex items-center ${timeLeft <= 10 && !gameOver ? 'text-red-400 animate-pulse' : ''}`}>
          {/* SVG icon for timer */}
          <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          Time: {formatTime(timeLeft)}
        </span>
      </div>

      {/* Game Board */}
      <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-4 lg:grid-cols-4 gap-4 p-4 md:p-6 bg-white bg-opacity-10 rounded-xl shadow-2xl max-w-screen-lg w-full mb-8">
        {cards.map((card) => (
          <Card
            key={card.id}
            card={card}
            onClick={handleCardClick}
            flippedCardsIds={flippedCards.map(fc => fc.id)} // Pass IDs of currently flipped cards
            matchedCardsIds={matchedCards} // Pass IDs of matched cards
          />
        ))}
      </div>

      {/* Game Over Message (Win or Time Out) */}
      {gameOver && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 animate-fade-in">
          <div className="bg-white text-gray-900 rounded-xl p-8 shadow-2xl text-center max-w-sm w-full transform scale-105 animate-bounce-in">
            {timeLeft > 0 ? (
              <>
                <h2 className="text-3xl font-bold mb-4">You did it! 🎉</h2>
                <p className="text-xl mb-6">All variables matched in {moves} moves!</p>
              </>
            ) : (
              <>
                <h2 className="text-3xl font-bold mb-4 text-red-600">Time's Up! ⏰</h2>
                <p className="text-xl mb-6">You ran out of time. Try again!</p>
              </>
            )}
            <button
              onClick={resetGame}
              className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-lg transition duration-300 ease-in-out transform hover:scale-105 shadow-lg"
            >
              Play Again
            </button>
          </div>
        </div>
      )}

      {/* Pursuit Builder Cohort Link */}
      <div className="mt-8 text-center">
        <p className="text-xl mb-4">Interested in becoming a builder?</p>
        <a
          href="https://pursuit.org/cohorts" // REMINDER: Update this URL!
          target="_blank"
          rel="noopener noreferrer"
          className="bg-yellow-400 hover:bg-yellow-500 text-gray-900 font-bold py-3 px-8 rounded-full transition duration-300 ease-in-out transform hover:scale-105 shadow-lg text-lg flex items-center justify-center mx-auto max-w-xs"
        >
          <svg className="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.653-.169-1.277-.47-1.823M7 20h4V10H7v10zm0 0c-.824 0-1.614-.23-2.31-.664m2.31.664H5.429C4.437 20 4 19.563 4 18.571V10c0-.992.437-1.429 1.429-1.429h.573a2.25 2.25 0 00.558-.168M17 20v-9a2 2 0 00-2-2h-3l2-2m0 0l-2 2"></path></svg>
          Join Pursuit Cohort
        </a>
      </div>
    </div>
  );
}

export default App;