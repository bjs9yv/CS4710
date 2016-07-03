import world.Robot;
import world.World;

import java.awt.Point;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.PriorityQueue;


public class MyRobot extends Robot{	
	
	int rows;
	int cols;
	Point destination;
	Point start;
	int HValues[][] = null;
	boolean uncertain = false;
	PriorityQueue<Node> openList = null;
	ArrayList<Node> openListSearchable = null;
	ArrayList<Node> closedList = new ArrayList<Node>();
	ArrayList<Node> currPath = new ArrayList<Node>();
	
	@Override
	public void travelToDestination() {
		Point start = super.getPosition();
		Node currNode = new Node(start,HValues[start.x][start.y],0,null);
		Comparator<Node> comparator = new NodeComparator();
		openList = new PriorityQueue<Node>(comparator);
		openListSearchable = new ArrayList<Node>();
		Node dest = null;
		if(!uncertain){
			dest = buildCertainPath(currNode);
		}
		else{
			dest = buildUncertainPath(currNode);
		}
		reconstructPath(dest);
	}
	
	public void moveTo(Node node){
		currPath.add(node);
		while(node.parent != null){
			currPath.add(node.parent);
			node = node.parent;
		}
		for(int i = currPath.size()-1; i >= 0; i--){
			super.move(currPath.get(i).location);
		}
	}
	
	public void returnToStart(){
		for(int i = 1; i< currPath.size(); i++){
			super.move(currPath.get(i).location);
		}
	}
	
	public Node buildUncertainPath(Node currNode){
		currPath = new ArrayList<Node>();
		moveTo(currNode);
		ArrayList<Node> candidates = getAdjacentNodes(currNode);	
		for(int i=0;i<candidates.size();i++){
			Node candidate = candidates.get(i);
			
			if(candidate.location.equals(destination)){
				return new Node(destination,0,0,candidate);
			}
			if(candidateInClosedList(candidate)){
				continue;
			}
			if(candidateInOpenList(candidate)){
				Node incumbent = getCandidateInOpenList(candidate);
				if(candidate.GValue + currNode.GValue < candidate.FValue){
					incumbent.parent = currNode;
				}	
			}
			else {
				openList.add(candidate);
				openListSearchable.add(candidate);
			}
		}
		returnToStart();
		currNode = openList.poll();
		closedList.add(currNode);
		openListSearchable.remove(currNode);
		return buildUncertainPath(currNode);	
	}
	
	public Node buildCertainPath(Node currNode){
		ArrayList<Node> candidates = getAdjacentNodes(currNode);		
		for(int i=0;i<candidates.size();i++){
			Node candidate = candidates.get(i);
			if(candidate.location.equals(destination)){
				return new Node(destination,0,0,candidate);
			}
			if(candidateInClosedList(candidate)){
				continue;
			}
			if(candidateInOpenList(candidate)){
				Node incumbent = getCandidateInOpenList(candidate);
				if(candidate.GValue + currNode.GValue < candidate.FValue){
					incumbent.parent = currNode;
				}	
			}
			else {
				openList.add(candidate);
				openListSearchable.add(candidate);
			}
		}
		currNode = openList.poll();
		closedList.add(currNode);
		openListSearchable.remove(currNode);
		return buildCertainPath(currNode);
	}
	
	public void reconstructPath(Node dest){
		ArrayList<Node> path = new ArrayList<Node>();
		while(dest.parent != null){
			path.add(dest.parent);
			dest = dest.parent;
		}
		for(int i = path.size()-2; i >= 0; i--){
			super.move(path.get(i).location);
		}
	}
	
	public boolean candidateInClosedList(Node candidate) {
		for(int i=0; i<closedList.size();i++){
			if(closedList.get(i).location.x == candidate.location.x && closedList.get(i).location.y == candidate.location.y){
				return true;
			}
		}
		return false;
	}

	public Node getCandidateInOpenList(Node candidate){
		for(int i=0; i<openListSearchable.size();i++){
			if(openListSearchable.get(i).location.x == candidate.location.x && openListSearchable.get(i).location.y == candidate.location.y){
				return openListSearchable.get(i);
			}
		}
		return null;
	}
	
	public boolean candidateInOpenList(Node candidate){
		for(int i=0; i<openListSearchable.size();i++){
			if(openListSearchable.get(i).location.x == candidate.location.x && openListSearchable.get(i).location.y == candidate.location.y){
				return true;
			}
		}
		return false;
	}
	
	public ArrayList<Node> getAdjacentNodes(Node node){
		ArrayList<Node>adjacents = new ArrayList<Node>();
		int i = node.location.x;
		int j = node.location.y;
		int horrizontalVerticalCost = 10;
		int diagonalCost = 14;
		if(i-1 >= 0){
			Point p1 = new Point(i-1,j);
			String pong1 = super.pingMap(p1);
			if(!pong1.equals("X")){
				int HValue = HValues[i-1][j];
				Node parent = node;
				int GValue = parent.GValue + horrizontalVerticalCost;
				Node n = new Node(p1,HValue,GValue,parent);
				adjacents.add(n);
			}
			if(j-1 >= 0){
				Point p2 = new Point(i-1,j-1);
				String pong2 = super.pingMap(p2);
				if(!pong2.equals("X")){
					int HValue = HValues[i-1][j-1];
					Node parent = node;
					int GValue = parent.GValue + diagonalCost;
					Node n = new Node(p2,HValue,GValue,parent);
					adjacents.add(n);
				}
			}
		}
		if(j+1 < cols){
			Point p1 = new Point(i,j+1);
			String pong1 = super.pingMap(p1);
			if(!pong1.equals("X")){
				int HValue = HValues[i][j+1];
				Node parent = node;
				int GValue = parent.GValue + horrizontalVerticalCost;
				Node n = new Node(p1,HValue,GValue,parent);
				adjacents.add(n);
			}
			if(i-1 >= 0){
				Point p2 = new Point(i-1,j+1);
				String pong2 = super.pingMap(p2);
				if(!pong2.equals("X")){
					int HValue = HValues[i-1][j+1];
					Node parent = node;
					int GValue = parent.GValue + diagonalCost;
					Node n = new Node(p2,HValue,GValue,parent);
					adjacents.add(n);
				}
			}
		}
		if(i+1 < rows){
			Point p1 = new Point(i+1,j);
			String pong1 = super.pingMap(p1);
			if(!pong1.equals("X")){
				int HValue = HValues[i+1][j];
				Node parent = node;
				int GValue = parent.GValue + horrizontalVerticalCost;
				Node n = new Node(p1,HValue,GValue,parent);
				adjacents.add(n);
			}
			if(j+1 < cols){
				Point p2 = new Point(i+1,j+1);
				String pong2 = super.pingMap(p2);
				if(!pong2.equals("X")){
					int HValue = HValues[i+1][j+1];
					Node parent = node;
					int GValue = parent.GValue + diagonalCost;
					Node n = new Node(p2,HValue,GValue,parent);
					adjacents.add(n);
				}
			}
		}
		if(j-1 >= 0){
			Point p1 = new Point(i,j-1);
			String pong1 = super.pingMap(p1);
			if(!pong1.equals("X")){
				int HValue = HValues[i][j-1];
				Node parent = node;
				int GValue = parent.GValue + horrizontalVerticalCost;
				Node n = new Node(p1,HValue,GValue,parent);
				adjacents.add(n);
			}
			if(i+1 < rows){
				Point p2 = new Point(i+1,j-1);
				String pong2 = super.pingMap(p2);
				if(!pong2.equals("X")){
					int HValue = HValues[i+1][j-1];
					Node parent = node;
					int GValue = parent.GValue + diagonalCost;
					Node n = new Node(p2,HValue,GValue,parent);
					adjacents.add(n);
				}
			}
		}
		return adjacents;
	}
	
	public int[][] preComputeH(World myWorld){
		Point dest = myWorld.getEndPos();
		cols = myWorld.numCols();
 		rows = myWorld.numRows();
 		HValues = new int[rows][cols];
 		for(int i=0;i<rows;i++){
 			for(int j=0;j<cols;j++){
 				HValues[i][j] = (int) (Math.abs(dest.getX()-i) + Math.abs(dest.getY()-j));
 			}
 		}
		return HValues;
	}
	
	@Override 
	public void addToWorld(World myWorld){
		uncertain = myWorld.getUncertain();
		destination = myWorld.getEndPos();
		start = myWorld.getStartPos();
		preComputeH(myWorld);
		super.addToWorld(myWorld);
	}

	public static void main(String[] args){
		try {
			World myWorld = new World ("myInputFile2.txt", false );	
			MyRobot myRobot = new MyRobot() ;
			myRobot.addToWorld(myWorld);
			myRobot.travelToDestination();
		}
		catch (Exception e) {
			e.printStackTrace () ;
		}
	}
}