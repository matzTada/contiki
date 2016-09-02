XML xml;

int zoom = 7;
String input_xml_file = "test.csc";
String input_pdr_file = "test.csv";
//String [] LINK_ARRAY = {
//  "1-2", "1-3", "2-3", "2-4", "3-5", "2-5", "3-4", "4-5", "4-6", "5-7", "4-7", "5-6", "6-7", "6-8", "7-8"
//};
String [] LINK_ARRAY= {
  "9-1", "9-2", "9-3", "2-3", "2-4", "3-5", "2-5", "3-4", "4-5", "4-6", "5-7", "4-7", "5-6", "6-7", "6-8", "7-8"
};
int NUM_DATA_SET = 20;

class Node {
  int id;
  float x, y;

  Node(int _id, float _x, float _y) {
    id = _id;
    x = _x;
    y = _y;
  }

  void display() {
    fill(255);
    stroke(0);
    strokeWeight((zoom > 4) ? (zoom / 4) : 2);
    ellipse(x, y, 5 * zoom, 5 * zoom);
    fill(0);
    textSize(4 * zoom);
    textAlign(CENTER, CENTER);
    text(str(id), x, y);
  }
}

void setup() {
  size(1200, 1200);
  background(255);
  int NUM_NODE = 0;

  //get position data from xml file
  xml = loadXML(input_xml_file);
  XML[] c1 = xml.getChildren("simulation");
  XML[] c2 = c1[0].getChildren("mote");
  NUM_NODE = c2.length;
  Node [] nodes = new Node[NUM_NODE];

  float x_avg = 0;
  float y_avg = 0;
  for (int i = 0; i < NUM_NODE; i++) {
    XML [] c3 = c2[i].getChildren("interface_config");
    int id = int(c3[2].getChild("id").getContent());
    float x = float(c3[0].getChild("x").getContent());
    float y = float(c3[0].getChild("y").getContent());
    x_avg += x * zoom;
    y_avg += y * zoom;
    nodes[i] = new Node(id, x * zoom, y * zoom);
    println(id + ", " + x + ", " + y);
  }

  //display
  x_avg /= (float)NUM_NODE;
  y_avg /= (float)NUM_NODE;
  translate(width/2 - x_avg, height/2 - y_avg); //centerize

  for (int run_id = 1; run_id < NUM_DATA_SET + 1; run_id++) {
    background(255);
    println("--- try run_id:" + str(run_id) + " ---");
    textAlign(DOWN, LEFT);
    fill(0);
    textSize(4 * zoom);
    text("dataset" + str(run_id), -(width/2 - x_avg), -(height/2 - y_avg) + textAscent());

    //get PDR_ARRAY from csv file
    int [] PDR_ARRAY = new int[LINK_ARRAY.length];  //  int [] PDR_ARRAY = {97, 48, 100, 99, 100, 98, 98, 74, 100, 93, 77, 94, 96, 43, 87};
    String[] lines = loadStrings(input_pdr_file);
    for (String tempLine : lines) {
      String[] items = split(tempLine, ",");
      if (items.length > LINK_ARRAY.length && int(split(items[0], ":")[1]) == run_id) {
        println("Find data");
        for (int i = 0; i < LINK_ARRAY.length; i++) {
          PDR_ARRAY[i] = int(items[i+1]);
        }
        break;
      }
    }

    int adjancency_pdr_matrix[][] = new int[LINK_ARRAY.length][LINK_ARRAY.length];
    for (int i = 0; i < LINK_ARRAY.length; i++) {
      int x = int(split(LINK_ARRAY[i], "-")[0]) - 1;
      int y = int(split(LINK_ARRAY[i], "-")[1]) - 1;
      adjancency_pdr_matrix[x][y] = PDR_ARRAY[i];
      adjancency_pdr_matrix[y][x] = PDR_ARRAY[i];
    }

    //display lines
    for (int i = 0; i < LINK_ARRAY.length; i++) {
      for (int j = 0; j < LINK_ARRAY.length; j++) {
        print(nf(adjancency_pdr_matrix[i][j], 3) + " ");
        if (adjancency_pdr_matrix[i][j] > 0) {
          stroke(get_link_color(adjancency_pdr_matrix[i][j]));
          strokeWeight(zoom);
          line(nodes[i].x, nodes[i].y, nodes[j].x, nodes[j].y);
          fill(0);
          textAlign(CENTER, CENTER);
          textSize(3 * zoom);
          text(str(adjancency_pdr_matrix[i][j]), (1 * nodes[i].x + 3 * nodes[j].x) / 4, (1 * nodes[i].y + 3 * nodes[j].y) / 4 );
        }
      }
      println("");
    }

    //display node circle
    for (int i = 0; i < NUM_NODE; i++) {
      nodes[i].display();
    }

    save("./data/dataset" + str(run_id) + "_topology.png");
  }

  println("----------- draw finish -----------");
  println("----------- draw finish -----------");
  println("----------- draw finish -----------");
  exit();
}

color get_link_color(int pdr) {
  //  println("pdr:" + pdr + ",map:" + str(map(pdr, 0, 100, 0, 50)));
  color c;
  //  if (pdr > 50) c = color(map(pdr, 50, 100, 0, 60), 50, 100, 50);
  //  else c = color(0, 50, 100);
  //for RGB
  c = color(127, 127, 127, 75);
  if (pdr == 100) c = color(0, 0, 255, 125);
  else if (pdr > 90) c = color(0, 0, 255, 75);
  else if (pdr > 75) c = color(0, 255, 0, 75);
  else if (pdr > 50) c = color(255, 256, 0, 75);
  else c = color(255, 0, 0, 75);
  return c;
}

