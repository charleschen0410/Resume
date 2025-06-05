package FeetInchestoCM_Converter;  

import javax.swing.*;

import java.awt.EventQueue;
import java.awt.event.*;

public class feetInchestoCM_Converter {

    private JFrame frame;
    private JTextField textFeet;
    private JTextField textInch;
    private JTextField textCm;
    private JLabel resultLabel1;
    private JLabel resultLabel2;

    public static void main(String[] args) {
        EventQueue.invokeLater(() -> {
            try {
            	feetInchestoCM_Converter window = new feetInchestoCM_Converter();
                window.frame.setVisible(true);
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }

    public feetInchestoCM_Converter() {
        initialize();
    }

    private void initialize() {
        frame = new JFrame("長度單位轉換器");
        frame.setBounds(100, 100, 500, 300);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.getContentPane().setLayout(null);

        JLabel lblFeet = new JLabel("英尺 (ft):");
        lblFeet.setBounds(30, 30, 100, 25);
        frame.getContentPane().add(lblFeet);

        textFeet = new JTextField();
        textFeet.setBounds(100, 30, 80, 25);
        frame.getContentPane().add(textFeet);

        JLabel lblInch = new JLabel("英吋 (in):");
        lblInch.setBounds(200, 30, 100, 25);
        frame.getContentPane().add(lblInch);

        textInch = new JTextField();
        textInch.setBounds(270, 30, 80, 25);
        frame.getContentPane().add(textInch);

        JButton btnToCm = new JButton("轉換成公分");
        btnToCm.setBounds(360, 30, 110, 25);
        frame.getContentPane().add(btnToCm);

        resultLabel1 = new JLabel("");
        resultLabel1.setBounds(30, 60, 400, 25);
        frame.getContentPane().add(resultLabel1);

        JLabel lblCm = new JLabel("公分 (cm):");
        lblCm.setBounds(30, 120, 100, 25);
        frame.getContentPane().add(lblCm);

        textCm = new JTextField();
        textCm.setBounds(100, 120, 80, 25);
        frame.getContentPane().add(textCm);

        JButton btnToFeetInch = new JButton("轉換成英尺/英吋");
        btnToFeetInch.setBounds(200, 120, 150, 25);
        frame.getContentPane().add(btnToFeetInch);

        resultLabel2 = new JLabel("");
        resultLabel2.setBounds(30, 150, 400, 25);
        frame.getContentPane().add(resultLabel2);

        btnToCm.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    double feet = Double.parseDouble(textFeet.getText());
                    double inch = Double.parseDouble(textInch.getText());
                    double totalInches = feet * 12 + inch;
                    double cm = totalInches * 2.54;

                    resultLabel1.setText(String.format("結果：%.2f 公分", cm));
                } catch (NumberFormatException ex) {
                    resultLabel1.setText("請輸入正確的數字格式！");
                }
            }
        });

        btnToFeetInch.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    double cm = Double.parseDouble(textCm.getText());
                    double totalInches = cm / 2.54;

                    int feet = (int)(totalInches / 12);
                    double inch = totalInches % 12;

                    resultLabel2.setText(String.format("結果：%d 英尺 %.2f 英吋", feet, inch));
                } catch (NumberFormatException ex) {
                    resultLabel2.setText("請輸入正確的數字格式！");
                }
            }
        });
    }
}
