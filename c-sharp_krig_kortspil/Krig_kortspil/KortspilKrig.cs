using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Krig_kortspil
{
    public class KortspilKrig
    {
        Dealer dealer;

        Player playerOne;
        Player playerTwo;

        int roundNum = 0;

        int beepFrequency = 500;
        int beepDuration = 500;

        int maxRounds = 1000000;

        private int MaxRounds 
        { 
            get { return maxRounds; } 
            set 
            { 
                if (value <= 0) 
                {
                    maxRounds = 1;
                }
                else
                {
                    maxRounds = value;
                }
            } 
        }

        /// <summary>
        /// Constructor with default maxRounds (1000000)
        /// </summary>
        /// <param name="namePlayerOne">Name of player one</param>
        /// <param name="namePlayerTwo">'Name of player two</param>
        public KortspilKrig(string namePlayerOne, string namePlayerTwo)
        {
            Initialize();

            this.playerOne = new Player(namePlayerOne, dealer.DealCards(2));
            this.playerTwo = new Player(namePlayerTwo, dealer.DealCards(2));
        }

        /// <summary>
        /// Constuctor with custom maxRounds
        /// </summary>
        /// <param name="namePlayerOne">Name of player one</param>
        /// <param name="namePlayerTwo">'Name of player two</param>
        /// <param name="maxRounds">Number of max rounds</param>
        public KortspilKrig(string namePlayerOne, string namePlayerTwo, int maxRounds)
        {
            Initialize();

            this.playerOne = new Player(namePlayerOne, dealer.DealCards(2));
            this.playerTwo = new Player(namePlayerTwo, dealer.DealCards(2));

            this.MaxRounds = maxRounds;
        }

        /// <summary>
        /// Initialize a game of Krig
        /// </summary>
        private void Initialize()
        {
            dealer = new Dealer();
            dealer.Reset();
            dealer.ShuffleCards();
        }

        /// <summary>
        /// Start a game of Krig
        /// </summary>
        /// <param name="PlayerOne">Player one</param>
        /// <param name="PlayerTwo">Player two</param>
        public void StartGame()
        {
            while (playerOne.NumCards > 0 && playerTwo.NumCards > 0 && roundNum <= maxRounds)
            {
                Round();
            }

            if (roundNum > MaxRounds)
            {
                if (playerOne.NumCards == playerTwo.NumCards)
                {
                    Console.WriteLine("Both players died of age exactly at the same time");
                }
                else
                {
                    Player dieWinner = playerOne.NumCards > playerTwo.NumCards ? playerOne : playerTwo;
                    Player dieLoser = playerOne.NumCards < playerTwo.NumCards ? playerOne : playerTwo;
                    Console.WriteLine($"\nBoth players died of age, but {dieWinner} lived a little bit longer than {dieLoser}");
                }

                ShowStats();
            }
            else
            {
                CheckForWinner();
            }
            
            Console.Beep(beepFrequency, beepDuration);
        }

        /// <summary>
        /// Run a single round
        /// </summary>
        public void Round()
        {
            // Increase round number
            roundNum++;

            Console.WriteLine($"Num Cards before round: {playerOne} has {playerOne.NumCards} and {playerTwo} has {playerTwo.NumCards}");


            // Each player draws one card
            Card cardOne = playerOne.NextCard();
            Card cardTwo = playerTwo.NextCard();

            Console.WriteLine($"Round {roundNum} : {cardOne.Rank} <> {cardTwo.Rank}\n");

            // See who won this round
            if (cardOne.Rank == cardTwo.Rank)
            {
                Krig(cardOne, cardTwo);
            }
            else if (cardOne.Rank > cardTwo.Rank)
            {
                playerOne.GetCards(cardOne, cardTwo);
                playerOne.RoundsWon++;
            }
            else if (cardOne.Rank < cardTwo.Rank)
            {
                playerTwo.GetCards(cardOne, cardTwo);
                playerTwo.RoundsWon++;
            }
        }

        /// <summary>
        /// Krig!
        /// </summary>
        /// <param name="cardOne">Card from PlayerOne</param>
        /// <param name="cardTwo">Card from PlayerTwo</param>
        public void Krig(Card cardOne, Card cardTwo)
        {
            Console.WriteLine($"Krig! {cardOne.Rank} <> {cardTwo.Rank}\n");

            int numExtraCards;

            if (playerOne.NumCards >= 3 && playerTwo.NumCards >= 3)
            {
                numExtraCards = 3;
            }
            else
            {
                numExtraCards = Math.Min(playerOne.NumCards, playerTwo.NumCards);
            }

            
            Card[] extraCardsTwo = new Card[numExtraCards];
            Card[] extraCardsOne = new Card[numExtraCards];

            // Get the next three cards from PlayerOne
            for (int i = 0; i < numExtraCards; i++)
            {
                extraCardsOne[i] = playerOne.NextCard();
            }

            // Get the next three cards from PlayerTwo
            for (int i = 0; i < numExtraCards; i++)
            {
                extraCardsTwo[i] = playerTwo.NextCard();
            }

            int pointOne = 0;
            int pointTwo = 0;

            // Compare each pair of cards and give point to the winning player for each pair won
            for (int i = 0; i < numExtraCards; i++)
            {
                Card cardExtraOne = extraCardsOne[i];
                Card cardExtraTwo = extraCardsTwo[i];

                if (cardExtraOne.Rank > cardExtraTwo.Rank)
                {
                    pointOne++;
                }
                else if (cardExtraOne.Rank < cardExtraTwo.Rank)
                {
                    pointTwo++;
                }
            }

            // Add cardOne, cardTwo and all extra cards to one list
            List<Card> cardsToWin = new List<Card>();

            cardsToWin.Add(cardOne);
            cardsToWin.Add(cardTwo);
            cardsToWin.AddRange(extraCardsOne);
            cardsToWin.AddRange(extraCardsTwo);

            // Choose a winner based on the points the players have
            if (pointOne > pointTwo)
            {
                playerOne.GetCards(cardsToWin);
                playerOne.KrigWon++;
            }
            else if (pointOne < pointTwo)
            {
                playerTwo.GetCards(cardsToWin);
                playerTwo.KrigWon++;
            }
            else
            {
                Random rnd = new Random();

                int rndNum = rnd.Next(2);

                // Pick a random winner
                if (rndNum == 0)
                {
                    playerOne.GetCards(cardsToWin);
                    playerOne.KrigWon++;
                }
                else
                {
                    playerTwo.GetCards(cardsToWin);
                    playerOne.KrigWon++;
                }
            }
        }

        /// <summary>
        /// Check for a winner
        /// </summary>
        /// <returns>Return true if there is a winner</returns>
        private void CheckForWinner()
        {
            // Check if a player has zero cards
            if (playerOne.NumCards == 0 || playerTwo.NumCards == 0)
            {
                Player winner = playerOne.NumCards == 0 ? playerTwo : playerOne;

                Console.WriteLine($"Winner is {winner}");

                ShowStats();

                Console.Beep(beepFrequency, beepDuration);
            }
        }

        private void ShowStats()
        {
            Console.WriteLine("\nStats:");
            Console.WriteLine($"Total rounds: {roundNum}");
            Console.WriteLine($"Rounds won: {playerOne} won {playerOne.RoundsWon} rounds\n" +
                              $"            {playerTwo} won {playerTwo.RoundsWon} rounds");
            Console.WriteLine($"Krigs won: {playerOne} won {playerOne.KrigWon} krigs\n" +
                              $"           {playerTwo} won {playerTwo.KrigWon} krigs");
            Console.WriteLine($"Num cards: {playerOne} has {playerOne.NumCards} cards\n" +
                              $"           {playerTwo} has {playerTwo.NumCards} cards");
        }
    }
}
