package sqlancer.common;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.lang.ProcessBuilder.Redirect;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class DBMSCommon {

    private static final Pattern SQLANCER_INDEX_PATTERN = Pattern.compile("^i\\d+");

    private DBMSCommon() {
    }

    public static String createTableName(int nr) {
        return String.format("t%d", nr);
    }

    public static String createColumnName(int nr) {
        return String.format("c%d", nr);
    }

    public static String createIndexName(int nr) {
        return String.format("i%d", nr);
    }

    public static boolean matchesIndexName(String indexName) {
        Matcher matcher = SQLANCER_INDEX_PATTERN.matcher(indexName);
        return matcher.matches();
    }

    public static int getMaxIndexInDoubleArray(double... doubleArray) {
        int maxIndex = 0;
        double maxValue = 0.0;
        for (int j = 0; j < doubleArray.length; j++) {
            double curReward = doubleArray[j];
            if (curReward > maxValue) {
                maxIndex = j;
                maxValue = curReward;
            }
        }
        return maxIndex;
    }

    public static boolean areQueryPlanSequencesSimilar(List<String> list1, List<String> list2) {
        return editDistance(list1, list2) <= 1;
    }

    public static int editDistance(List<String> list1, List<String> list2) {
        int[][] dp = new int[list1.size() + 1][list2.size() + 1];
        for (int i = 0; i <= list1.size(); i++) {
            for (int j = 0; j <= list2.size(); j++) {
                if (i == 0) {
                    dp[i][j] = j;
                } else if (j == 0) {
                    dp[i][j] = i;
                } else {
                    dp[i][j] = Math.min(dp[i - 1][j - 1] + costOfSubstitution(list1.get(i - 1), list2.get(j - 1)),
                            Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1));
                }
            }
        }
        return dp[list1.size()][list2.size()];
    }

    private static int costOfSubstitution(String string, String string2) {
        return string.equals(string2) ? 0 : 1;
    }

    public static String parseQueryPlan(String queryPlan, String db, String application, String pathUplan) {
        String parsedQueryPlan = "";
        try {
            ProcessBuilder pb = new ProcessBuilder("python3", "main.py", "-a", application, "-t", db);
            pb.directory(new java.io.File(pathUplan));
            pb.redirectInput(Redirect.PIPE);
            Process p = pb.start();
            OutputStream os = p.getOutputStream();
            os.write(queryPlan.getBytes());
            os.flush();
            os.close();
            InputStream is = p.getInputStream();
            BufferedReader br = new BufferedReader(new InputStreamReader(is));
            String line = null;
            while ((line = br.readLine()) != null) {
                parsedQueryPlan += line;
            }
            // Wait for the process to finish and get the exit code
            if (p.waitFor() != 0) {
                InputStream es = p.getErrorStream();
                BufferedReader er = new BufferedReader(new InputStreamReader(es));
                line = null;
                while ((line = er.readLine()) != null) {
                    System.out.println(line);
                }
                System.out.println("-------------------");
                System.out.println(queryPlan);
                System.out.println("-------------------");
                throw new Exception("Error while parsing query plan");
            }
        } catch (Exception e) {
            e.printStackTrace();
        } 
        return parsedQueryPlan;
    }

}
