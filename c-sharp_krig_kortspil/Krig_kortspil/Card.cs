using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Krig_kortspil
{
    public class Card
    {
        private Suits suit;
        private Ranks rank;

        /// <summary>
        /// Suit of the card
        /// </summary>
        public Suits Suit { get => suit; }

        /// <summary>
        /// Rank of the card
        /// </summary>
        public Ranks Rank { get => rank; }

        /// <summary>
        /// Card constructor
        /// </summary>
        /// <param name="suit">Suit for the card</param>
        /// <param name="rank">Rank for the card</param>
        public Card(Suits suit, Ranks rank)
        {
            this.suit = suit;
            this.rank = rank;
        }

        public override string ToString()
        {
            return $"{rank} of {suit}";
        }
    }
}
