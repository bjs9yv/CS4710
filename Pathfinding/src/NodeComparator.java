import java.util.Comparator;

public class NodeComparator implements Comparator<Node> {

	@Override
	public int compare(Node n1, Node n2) {
		if(n1.FValue <= n2.FValue){
			return -1;
		}
		else {
			return 1;
		}
	}
}
