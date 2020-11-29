using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Krig_kortspil
{
    /// <summary>
    /// Responsible for giving out cards to players, shuffle and reset card deck etc.
    /// </summary>
    class Dealer
    {
        private List<Card> cardDeck;

        /// <summary>
        /// Current cards in card deck
        /// </summary>
        public List<Card> CardDeck { get => cardDeck; }

        /// <summary>
        /// Dealer constructor
        /// </summary>
        public Dealer()
        {
            cardDeck = new List<Card>();
        }

        /// <summary>
        /// Reset card deck without shuffling
        /// </summary>
        public void Reset()
        {
            cardDeck.Clear();

            // Loop through all suits
            foreach (Suits suit in Enum.GetValues(typeof(Suits)))
            {
                // Loop through all ranks
                foreach (Ranks rank in Enum.GetValues(typeof(Ranks)))
                {
                    cardDeck.Add(new Card(suit, rank));
                }
            }
        }

        /// <summary>
        /// Shuffle card in deck
        /// </summary>
        public void ShuffleCards()
        {
            cardDeck.Shuffle();
        }

        /// <summary>
        /// Deal cards out once
        /// </summary>
        /// <param name="numPlayers">Number of players playing</param>
        /// <returns>List of cards to a player</returns>
        public List<Card> DealCards(int numPlayers)
        {
            List<Card> cardsToGive = new List<Card>();

            int numOfCardsToGive = Math.Abs(52 / numPlayers);

            Random rnd = new Random();

            for (int i = 0; i < numOfCardsToGive; i++)
            {
                Card cardToGive = cardDeck[rnd.Next(0, cardDeck.Count)];
                cardsToGive.Add(cardToGive);
                cardDeck.Remove(cardToGive);
            }

            return cardsToGive;
        }

    }
}
