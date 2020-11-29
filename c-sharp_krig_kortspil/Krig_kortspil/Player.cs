using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Krig_kortspil
{
    public class Player
    {
        /// <summary>
        /// Name of player
        /// </summary>
        public string Name { get; private set; }

        /// <summary>
        /// Number of rounds player has won
        /// </summary>
        public int RoundsWon { get; set; }
        
        /// <summary>
        /// Number of Krig player has won
        /// </summary>
        public int KrigWon { get; set; }

        /// <summary>
        /// Cards the player has
        /// </summary>
        //public PlayerHand Hand;

        //public int startNumCards;

        //public List<Card> startCards;

        //public List<Card> cards;

        /// <summary>
        /// Queue to take cards from
        /// </summary>
        private Queue<Card> queueCards = new Queue<Card>();

        /// <summary>
        /// Number of cards on player's hand
        /// </summary>
        public int NumCards { get => queueCards.Count; }

        /// <summary>
        /// Player constructor with custom name and list of cards
        /// </summary>
        /// <param name="name">Name for player</param>
        /// <param name="cards">List of cards to player</param>
        public Player(string name, List<Card> cards)
        {
            this.Name = name;
            this.RoundsWon = 0;
            this.KrigWon = 0;
            //this.Hand.cards = cards;
            //this.Hand.startCards = cards;
            //this.Hand.startNumCards = cards.Count;
            //this.cards = cards;
            //this.startCards = cards;
            //this.startNumCards = cards.Count;
            AddCardsToQueue(cards);
        }

        /// <summary>
        /// Add cards on players hand to queue
        /// </summary>
        private void AddCardsToQueue(List<Card> cards)
        {
            foreach (Card card in cards)
            {
                queueCards.Enqueue(card);
            }
        }

        /// <summary>
        /// Add two cards to hand
        /// </summary>
        /// <param name="cardOne">The first card to get</param>
        /// <param name="cardTwo">The second card to get</param>
        public void GetCards(Card cardOne, Card cardTwo)
        {
            //cards.Add(card);
            queueCards.Enqueue(cardOne);
            queueCards.Enqueue(cardTwo);
        }

        /// <summary>
        /// Add every card to hand from a list of cards
        /// </summary>
        /// <param name="cards">List of cards to add to hand</param>
        public void GetCards(List<Card> cards)
        {
            foreach (Card card in cards)
            {
                queueCards.Enqueue(card);
            }
        }

        /// <summary>
        /// Get the next card from the player's hand
        /// </summary>
        /// <returns>The next card in player's hand</returns>
        public Card NextCard()
        {
            Card nextCard = queueCards.Dequeue();
            //cards.Remove(nextCard);
            return nextCard;
        }

        public override string ToString()
        {
            return $"{Name}";
        }
    }
}
