// 定义Person接口
interface Person {
    String getId();
    String getName();
    String getGender();
    double calculateTotalScore();
    double calculateAverageScore();
    String getGrade();
}

// 定义Student父类
class Student implements Person {
    protected String id;
    protected String name;
    protected String gender;
    protected double[] scores;

    public Student(String id, String name, String gender, double[] scores) {
        this.id = id;
        this.name = name;
        this.gender = gender;
        this.scores = scores;
    }

    @Override
    public String getId() {
        return id;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public String getGender() {
        return gender;
    }

    @Override
    public double calculateTotalScore() {
        double total = 0;
        for (double score : scores) {
            total += score;
        }
        return total;
    }

    @Override
    public double calculateAverageScore() {
        return calculateTotalScore() / scores.length;
    }

    @Override
    public String getGrade() {
        double average = calculateAverageScore();
        if (average >= 90) {
            return "A";
        } else if (average >= 80) {
            return "B";
        } else if (average >= 70) {
            return "C";
        } else if (average >= 60) {
            return "D";
        } else {
            return "F";
        }
    }
}

// 定义Ungraduate子类
class Ungraduate extends Student {
    public Ungraduate(String id, String name, String gender, double[] scores) {
        super(id, name, gender, scores);
    }
}

// 定义Graduate子类
class Graduate extends Student {
    private String researchDirection;
    private String tutor;

    public Graduate(String id, String name, String gender, double[] scores, String researchDirection, String tutor) {
        super(id, name, gender, scores);
        this.researchDirection = researchDirection;
        this.tutor = tutor;
    }

    public String getResearchDirection() {
        return researchDirection;
    }

    public String getTutor() {
        return tutor;
    }

    @Override
    public String getGrade() {
        double average = calculateAverageScore();
        if (average >= 95) {
            return "A+";
        } else if (average >= 90) {
            return "A";
        } else if (average >= 85) {
            return "B+";
        } else if (average >= 80) {
            return "B";
        } else if (average >= 75) {
            return "C+";
        } else if (average >= 70) {
            return "C";
        } else if (average >= 65) {
            return "D+";
        } else if (average >= 60) {
            return "D";
        } else {
            return "F";
        }
    }
}

// 测试代码Text
public class StudentTest {
    public static void main(String[] args) {
        Ungraduate ungraduate = new Ungraduate("1", "张三", "男", new double[]{80, 85, 90});
        System.out.println("本科生信息：");
        System.out.println("学号：" + ungraduate.getId());
        System.out.println("姓名：" + ungraduate.getName());
        System.out.println("性别：" + ungraduate.getGender());
        System.out.println("总成绩：" + ungraduate.calculateTotalScore());
        System.out.println("平均成绩：" + ungraduate.calculateAverageScore());
        System.out.println("成绩等级：" + ungraduate.getGrade());

        Graduate graduate = new Graduate("2", "李四", "女", new double[]{85, 90, 95}, "计算机科学", "王教授");
        System.out.println("研究生信息：");
        System.out.println("学号：" + graduate.getId());
        System.out.println("姓名：" + graduate.getName());
        System.out.println("性别：" + graduate.getGender());
        System.out.println("研究方向：" + graduate.getResearchDirection());
        System.out.println("导师：" + graduate.getTutor());
        System.out.println("总成绩：" + graduate.calculateTotalScore());
        System.out.println("平均成绩：" + graduate.calculateAverageScore());
        System.out.println("成绩等级：" + graduate.getGrade());
    }
}
