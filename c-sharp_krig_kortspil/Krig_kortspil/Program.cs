using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Krig_kortspil
{
    class Program
    {
        static void Main(string[] args)
        {
            //StartKrig();

            string playerOneName = "Nik";
            string playerTwoName = "Luk";

            KortspilKrig krig = new KortspilKrig(playerOneName, playerTwoName);
            krig.StartGame();

            Console.ReadLine();
        }

        /// <summary>
        /// Start a game of the card game "Krig"
        /// </summary>
        static void StartKrig()
        {

            Dealer dealer = new Dealer();

            dealer.Reset();
            dealer.ShuffleCards();

            //for (int i = 0; i < dealer.CardDeck.Count; i++)
            //{
            //    Console.WriteLine($"Card {i} > {dealer.CardDeck[i]}");
            //}

            const int numPlayers = 2;
            //int numPlayers = Convert.ToInt32(Console.ReadLine());


             Player[] players = new Player[numPlayers];

            players[0] = new Player("Nik", dealer.DealCards(numPlayers));
            players[1] = new Player("Luk", dealer.DealCards(numPlayers));


            //foreach (Player player in players)
            //{
            //    int i = 0;
            //    foreach (Card card in player.startCards)
            //    {
            //        i++;
            //        Console.WriteLine($"{i} {player.Name} : {card}");
            //        Card hej = player.NextCard();
            //    }
            //}


            //KortspilKrig.StartGame(players[0], players[1]);


            Console.WriteLine();

            Console.WriteLine($"Left in deck:");
            foreach (Card card in dealer.CardDeck)
            {
                Console.WriteLine(card);
            }
        }
    }
}
