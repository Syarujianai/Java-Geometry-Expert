/**
 * Created by IntelliJ IDEA.
 * User: Ye
 * Date: 2006-2-18
 * Time: 21:26:51
 * To change this template use File | Settings | File Templates.
 */
package gprover;

import org.omg.CORBA.portable.InputStream;

import javax.swing.*;
import javax.swing.filechooser.FileFilter;
import java.io.*;

public class Main2 {
    public static void main(String[] args) {

//    final public static int CM_EX_PARA = 1;
//    final public static int CM_EX_ORTH = 2;
//    final public static int CM_EX_SIMSON = 3;
//    final public static int CM_EX_SQ = 4;
//    final public static int CM_EX_PAPPUS = 5;
//    final public static int CM_EX_PEDAL = 6;
//    final public static int CM_EX_MIQ1 = 7;

        String user_directory = System.getProperty("user.dir");
        String sp = System.getProperty("file.separator");
        // String dr = user_directory + sp + "ex";
        String dr = user_directory + sp + "output\\examples\\Junior Mathematics\\";
        JFileChooser chooser = new JFileChooser();
        chooser.setCurrentDirectory(new File(dr));
        int result = chooser.showOpenDialog(null);
        if (result == JFileChooser.CANCEL_OPTION) return;
        gterm gt = new gterm();
        try {
            // File file_1 = chooser.getSelectedFile();
            // gt.readAterm(new DataInputStream (new FileInputStream(chooser.getSelectedFile())));
            gt.readAterm(new BufferedReader(new FileReader(chooser.getSelectedFile())));
            Prover.set_gterm(gt);
            // Prover.run();
            Boolean t = Prover.prove();
            // cond dp = Prover.getProveHead();
            System.out.println(t);
//            gdd_bc db = new gdd_bc();
//            db.init_dbase();
//            db.setExample(gt);
//            db.sbase();
//            db.fixpoint();
//            db.show_fproof();


        } catch (IOException ee) {
        }

        //CMisc.print(Cm.s2077);
    }
}
