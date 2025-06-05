//統資二甲 陳彥嘉 412421446
package Game_NumberMemory;

import java.util.Random; // 隨機數生成器
import java.util.Scanner; // 用於讀取使用者輸入

public class game_NumberMemory {
    public static void main(String[] args) {
        /*
         * 數字記憶挑戰遊戲
         *
         * 遊戲規則： 
         * 1. 系統隨機生成一組數字，並在螢幕上顯示數秒。
         * 2. 數秒後，數字會被隱藏。
         * 3. 玩家需要準確輸入剛剛看到的數字。
         * 4. 若玩家輸入正確，顯示成功訊息；否則顯示失敗訊息並結束遊戲。
         *
         * 遊戲特點： 
         * - 玩家可以自訂數字的長度。
         * - 防呆機制：確保輸入為正確的數字格式。
         * - 遊戲難度可隨數字長度增大而提升。
         */

        Scanner scanner = new Scanner(System.in);
        System.out.println("歡迎來到數字記憶挑戰遊戲！");

        // 設定數字長度
        System.out.print("請輸入數字長度 (建議 3 至 10)：");
        int length = scanner.nextInt();
        while (length < 3 || length > 10) {
            System.out.print("長度不合理！請重新輸入 (3 至 10)：");
            length = scanner.nextInt();
        }

        // 生成隨機數字
        int[] randomNumber = generateRandomNumber(length);
        System.out.println("準備記住以下數字：");
        displayNumber(randomNumber);

        // 等待數秒後清屏
        try {
            Thread.sleep(2000); // 等待 3 秒
        } catch (InterruptedException e) {
            System.out.println("發生錯誤，遊戲結束。");
            return;
        }
        clearScreen();

        // 玩家輸入數字
        System.out.print("請輸入剛剛看到的數字：");
        String userInput = scanner.next();

        // 驗證結果
        if (isCorrect(randomNumber, userInput)) {
            System.out.println("恭喜你，記憶正確！");
        } else {
            System.out.println("很遺憾，記憶錯誤。正確答案是：" + arrayToString(randomNumber));
        }
        scanner.close();
    }

    // 隨機生成指定長度的數字
    private static int[] generateRandomNumber(int length) {
        Random random = new Random();
        int[] number = new int[length];
        for (int i = 0; i < length; i++) {
            number[i] = random.nextInt(10); // 0 至 9
        }
        return number;
    }

    // 顯示數字陣列
    private static void displayNumber(int[] number) {
        for (int n : number) {
            System.out.print(n);
        }
        System.out.println();
    }

    // 清空螢幕 (模擬效果)
    private static void clearScreen() {
        for (int i = 0; i < 50; i++) {
            System.out.println();
        }
    }

    // 檢查玩家輸入是否正確
    private static boolean isCorrect(int[] number, String input) {
        if (input.length() != number.length) {
            return false;
        }
        for (int i = 0; i < number.length; i++) {
            if (number[i] != Character.getNumericValue(input.charAt(i))) {
                return false;
            }
        }
        return true;
    }

    // 將陣列轉為字串
    private static String arrayToString(int[] array) {
        StringBuilder sb = new StringBuilder();
        for (int n : array) {
            sb.append(n);
        }
        return sb.toString();
    }
}
