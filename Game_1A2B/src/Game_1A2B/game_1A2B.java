//41241446 統資二甲 陳彥嘉
package Game_1A2B;

import java.util.*;

public class game_1A2B {

	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);

		// 讓玩家選擇要玩的位數
		int numDigits = 0;
		while (true) {
			System.out.println("Enter the number of digits you want to play (at least 3 digits):");
			numDigits = sc.nextInt();
			if (numDigits >= 3) { // 必須至少 3 位數
				break;
			} else {
				System.out.println("The number of digits must be at least 3.");
			}
		}

		// 生成隨機數字
		int lowerBound = (int) Math.pow(10, numDigits - 1); // 最小值為 100...（依照位數）
		int upperBound = (int) Math.pow(10, numDigits) - 1; // 最大值為 999...（依照位數）

		int temp = my_random(lowerBound, upperBound); // 生成隨機數字
		System.out.println("Answer (for debugging purposes): " + temp); // 顯示隨機數字，僅用於除錯

		int[] ans = new int[numDigits]; // 答案陣列
		int[] guess = new int[numDigits]; // 玩家猜的數字陣列
		splitter(temp, ans); // 將隨機數字拆解成陣列

		int a, b;
		do {
			a = 0;
			b = 0;
			int guessNumber = 0;

			// 確保玩家輸入的是正確位數的數字
			while (true) {
				System.out.println("Enter a " + numDigits + "-digit integer: ");
				guessNumber = sc.nextInt();

				// 檢查輸入的數字是否正確的位數
				if (guessNumber >= lowerBound && guessNumber <= upperBound) {
					break; // 若是正確位數，跳出循環
				} else {
					System.out.println("Invalid input. Please enter a " + numDigits + "-digit number.");
				}
			}

			splitter(guessNumber, guess); // 分割玩家的猜測數字

			// 用來標記已經匹配過的數字
			boolean[] usedAnswer = new boolean[numDigits]; // 追蹤答案中已經比對過的數字
			boolean[] usedGuess = new boolean[numDigits]; // 追蹤猜測中已經比對過的數字

			// 第一輪：檢查數字與位置是否完全相符 (A)
			for (int i = 0; i < ans.length; i++) {
				if (ans[i] == guess[i]) {
					a++; // 完全正確的數字與位置
					usedAnswer[i] = true; // 標記該位置已比對
					usedGuess[i] = true; // 標記該位置已猜對
				}
			}

			// 第二輪：檢查數字正確但是位置錯誤 (B)
			for (int i = 0; i < ans.length; i++) {
				if (!usedGuess[i]) { // 如果這個數字還沒被使用
					for (int j = 0; j < guess.length; j++) {
						if (!usedAnswer[j] && ans[j] == guess[i]) {
							b++; // 數字正確但是位置錯誤
							usedAnswer[j] = true; // 標記該位置已比對
							break;
						}
					}
				}
			}

			System.out.printf("You get %dA%dB.\n", a, b); // 顯示結果

		} while (a != numDigits); // 如果所有數字和位置都正確，遊戲結束

		System.out.println("Bingo!! Game is over.");
	}

	// 生成隨機數字，範圍從 lb 到 ub
	public static int my_random(int lb, int ub) {
		return ((int) (Math.random() * (ub - lb + 1)) + lb);
	}

	// 將數字拆分為每一位，並放入陣列
	public static void splitter(int n, int[] a) {
		for (int i = a.length - 1; i >= 0; i--) { // 這裡從最後一位開始處理
			a[i] = n % 10;
			n /= 10;
		}
	}
}
/*
 * package week15; import java.util.*; public class W15 {
 * 
 * public static void main(String[] args) { int temp=my_random(1000,9999);
 * System.out.println(temp);//先看答案 除錯用 int [] ans = new int [4];//答案的四個位數放數字 int
 * [] guess = new int [4];//玩家猜的數字四位數字放置處 splitter(temp,ans); for (int
 * i=0;i<ans.length;i++)//將ans陣列的內容依序列出 除錯用 System.out.println(ans[i]); Scanner
 * sc=new Scanner(System.in);
 * 
 * int a,b; do { a=0;b=0; System.out.println("Entry a 4-digit integer:>");
 * temp=sc.nextInt(); splitter(temp,guess); for(int
 * i=0;i<ans.length;i++)//將guess陣列的內容依序列出 除錯用 System.out.println(guess[i]);
 * for(int i=0;i<ans.length;i++) for(int j=0;j<guess.length;j++)
 * if(ans[i]==guess[j])//數字對 if (i==j)//位置也對 a++; else//位置不對 b++;
 * System.out.printf("You get %dA%dB.\n,",a,b); }while(a!=4);
 * System.out.println("Bingo!! Game is over."); } public static int
 * my_random(int lb,int ub) { return ((int)(Math.random()*(ub-lb)+lb)); } public
 * static void splitter(int n,int [] a) { for(int i=0;i<a.length;i++) {
 * a[i]=n%10; n/=10; }}}
 */
