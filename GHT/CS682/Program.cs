using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;

namespace CS682
{
	class MainClass
	{
		public static void Main (string[] args)
		{

			var n = new List<Point> {
				new Point (0, 0),
				new Point (0, 1),
				new Point (0, 2),
				new Point (1, 2),
				new Point (0, 3),
			};

			var m = new List<Point> {
				new Point (3, 1),
				new Point (3, 2),
				new Point (3, 3),
				new Point (4, 3),
				new Point (3, 4),
				new Point (4, 4),
				new Point (3, 5),
			};

			GHT (n, m, 8, 8);

			ChamferMatching (n, m, 8, 8);
		}

		public static void GHT (List<Point> template, List<Point> image, int w, int h)
		{
			var map = new int[h, w];

			var rows = template.Max (p => {
				return p.Y;
			});

			var cols = template.Max (p => {
				return p.X;
			});

			for (int i = 0; i < h - rows; i++) {
				for (int j = 0; j < w - cols; j++) {
					var s = 0;
					template.ForEach (p => {
						var tp = new Point (p.X + j, p.Y + i);
						if (image.Contains (tp))
							s++;
					});

					map [i, j] = s;
				}
			}
		
			OutputMap (map, h, w);
		}

		public static void ChamferMatching (List<Point> template, List<Point> image, int w, int h)
		{
			var D = new int[h, w];

			for (int i = 0; i < h; i++)
				for (int j = 0; j < w; j++)
					D [i, j] = 100;

			image.ForEach (p => D [p.Y, p.X] = 0);

			// forward pass

			for (int i = 0; i < h; i++)
				for (int j = 0; j < w; j++) {
					if (i > 0 && j > 0)
						D [i, j] = Math.Min (D [i, j], D [i - 1, j - 1] + 4);
					if (i > 0)
						D [i, j] = Math.Min (D [i, j], D [i - 1, j] + 4);
					if (i > 0 && j < w - 1)
						D [i, j] = Math.Min (D [i, j], D [i - 1, j + 1] + 4);
					if (j > 0)
						D [i, j] = Math.Min (D [i, j], D [i, j - 1] + 3);
				}

			OutputMap (D, h, w);

			// backwad pass
			for (int i = h - 1; i >= 0; i--)
				for (int j = w - 1; j >= 0; j--) {

					if (j < w - 1)
						D [i, j] = Math.Min (D [i, j], D [i, j + 1] + 3);
					if (i < h - 1 && j > 0)
						D [i, j] = Math.Min (D [i, j], D [i + 1, j - 1] + 4);
					if (i < h - 1)
						D [i, j] = Math.Min (D [i, j], D [i + 1, j] + 3);
					if (i < h - 1 && j < w - 1)
						D [i, j] = Math.Min (D [i, j], D [i + 1, j + 1] + 4);
				}

			OutputMap (D, h, w);

			var score = new int[h, w];

			for (int i = 0; i < h; i++)
				for (int j = 0; j < w; j++)
					score [i, j] = int.MaxValue;

			var rows = template.Max (p => {
				return p.Y;
			});

			var cols = template.Max (p => {
				return p.X;
			});

			for (int i = 0; i < h - rows; i++) {
				for (int j = 0; j < w - cols; j++) {
					var s = 0;
					template.ForEach (p => {
						var tp = new Point (p.X + j, p.Y + i);
						s += D [tp.Y, tp.X];
					});

					score [i, j] = s;
				}
			}

			OutputMap (score, h, w);
		}

		public static void OutputMap (int[,] map, int h, int w)
		{
			for (int i = 0; i < h; i++) {
				for (int j = 0; j < w; j++) {
					Console.Write ((map [i, j] >= 100 ? "X" : map [i, j].ToString ()) + "\t");
				}
				Console.WriteLine ();
			}

			Console.WriteLine ("-------------------------------------------------------------------------------------");
		}
	}
}
