package TripleDiceRoller;

import java.awt.EventQueue;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.SwingConstants;

public class tripleDiceRoller {

	private JFrame frame;
	private JLabel lblDice1, lblDice2, lblDice3, lblTotal;
	private Random random = new Random();

	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					tripleDiceRoller window = new tripleDiceRoller();
					window.frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	public tripleDiceRoller() {
		initialize();
	}

	private void initialize() {
		frame = new JFrame("麻將骰子模擬器 🎲");
		frame.setBounds(100, 100, 500, 360); // 加寬視窗
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().setLayout(null);

		// ✅ 修改：按鈕寬度變 200，字體適中
		JButton btnRoll = new JButton("猜猜骰到多少！");
		btnRoll.setFont(new Font("微軟正黑體", Font.BOLD, 18));
		btnRoll.setBounds(150, 30, 200, 50); // ✔ 加寬讓文字不會被擠掉
		frame.getContentPane().add(btnRoll);

		// 三顆骰子 Label（縮字＋加寬）
		lblDice1 = new JLabel("骰子壹號先生 ？");
		lblDice1.setHorizontalAlignment(SwingConstants.CENTER);
		lblDice1.setFont(new Font("微軟正黑體", Font.PLAIN, 18));
		lblDice1.setBounds(20, 100, 150, 40);
		frame.getContentPane().add(lblDice1);

		lblDice2 = new JLabel("骰子貳號先生 ？");
		lblDice2.setHorizontalAlignment(SwingConstants.CENTER);
		lblDice2.setFont(new Font("微軟正黑體", Font.PLAIN, 18));
		lblDice2.setBounds(175, 100, 150, 40);
		frame.getContentPane().add(lblDice2);

		lblDice3 = new JLabel("骰子參號先生 ？");
		lblDice3.setHorizontalAlignment(SwingConstants.CENTER);
		lblDice3.setFont(new Font("微軟正黑體", Font.PLAIN, 18));
		lblDice3.setBounds(330, 100, 150, 40);
		frame.getContentPane().add(lblDice3);

		// 顯示總和
		lblTotal = new JLabel("總和：？");
		lblTotal.setHorizontalAlignment(SwingConstants.CENTER);
		lblTotal.setFont(new Font("微軟正黑體", Font.BOLD, 24));
		lblTotal.setBounds(125, 180, 250, 50);
		frame.getContentPane().add(lblTotal);

		// 擲骰子事件
		btnRoll.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int d1 = random.nextInt(6) + 1;
				int d2 = random.nextInt(6) + 1;
				int d3 = random.nextInt(6) + 1;
				int total = d1 + d2 + d3;

				lblDice1.setText("骰子壹號先生 " + d1);
				lblDice2.setText("骰子貳號先生 " + d2);
				lblDice3.setText("骰子參號先生 " + d3);
				lblTotal.setText("總和：" + total);
			}
		});
	}
}
