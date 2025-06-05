//412421446 統資二甲 陳彥嘉
package Game_NumberGuessing;
import java.util.*;

public class game_NumberGuessing {
    public static void main(String[] args) {
        System.out.println("=== magic number==="); // 顯示遊戲標題
        int answer = my_random(1, 99); // 隨機生成1到99之間的數字作為答案
        
        int lb = 1, ub = 99; // 初始化上下界變數，初始值為1和99
        int guess; // 用於存放使用者輸入的猜測值
        boolean bingo = false; // 標記是否猜中答案
        Scanner sc = new Scanner(System.in); // 創建Scanner物件，用於接收使用者輸入

        while (!bingo) { // 進入遊戲迴圈，直到使用者猜中為止
            System.out.printf("Enter an integer between %d and %d.\n", lb, ub); // 提示使用者輸入範圍內的整數
            guess = sc.nextInt(); // 讀取使用者輸入的猜測值

            if (guess == answer) { // 判斷是否猜中答案
                bingo = true; // 標記猜中，退出迴圈
                System.out.println("BOOM!"); // 顯示猜中提示
            } else { // 如果沒有猜中
                if (guess <= lb || guess >= ub) { // 檢查使用者輸入是否在有效範圍內
                    System.out.println("請輸入範圍內的值"); // 如果不在範圍內，提示重新輸入
                }
                // 更新上下界
                if (guess > answer) { // 如果使用者的猜測值大於答案
                    ub = guess; // 更新上界為使用者的猜測值
                } else { // 如果使用者的猜測值小於答案
                    lb = guess; // 更新下界為使用者的猜測值
                }
            }
        }
    }

    // 生成隨機數的方法，返回 [low, up] 範圍內的隨機整數
    public static int my_random(int low, int up) {
        return (int)(Math.random() * (up - low + 1)) + low; // 隨機數公式，確保包含上下界
    }
}