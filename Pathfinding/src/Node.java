import java.awt.Point;

public class Node {
	Point location;
	int HValue;
	int GValue;
	int FValue;
	Node parent;
	
	public Node(Point l, int h, int g, Node p){
		this.location = l;
		this.HValue = h;
		this.GValue = g;
		this.FValue = HValue + GValue;
		this.parent = p;
	}
	
}
