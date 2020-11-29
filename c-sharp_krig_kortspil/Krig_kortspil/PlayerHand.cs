using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Krig_kortspil
{
    struct PlayerHand
    {
        /// <summary>
        /// Number of cards the player start with
        /// </summary>
        public int startNumCards;

        /// <summary>
        /// List with the cards the player starts with
        /// </summary>
        public List<Card> startCards;

        /// <summary>
        /// List with player's cards
        /// </summary>
        public List<Card> cards;
    }
}
