//
//  RecentstatViewController.swift
//  Shanti - Mental Health App
//
//  Created by Jahnavi Bavuluri  on 7/19/20.
//  Copyright © 2020 Jahnavi Bavuluri . All rights reserved.
//

import UIKit

class RecentstatViewController: UIViewController {
    
    @IBOutlet weak var mainView: UIView!
    
    @IBOutlet weak var progressbar: UIView!
    @IBOutlet weak var rmprogressbar: UIView!
    @IBOutlet weak var pwprogressbar: UIView!
    @IBOutlet weak var ntprogressbar: UIView!
    @IBOutlet weak var scprogressbar: UIView!
    @IBOutlet weak var dmprogressbar: UIView!
    @IBOutlet weak var sprogressbar: UIView!
    @IBOutlet weak var eprogressbar: UIView!
    @IBOutlet weak var cprogressbar: UIView!
    @IBOutlet weak var overallPerc: UILabel!
    @IBOutlet weak var rmPerc: UILabel!
    @IBOutlet weak var pwPerc: UILabel!
    @IBOutlet weak var ntPerc: UILabel!
    @IBOutlet weak var scPerc: UILabel!
    @IBOutlet weak var dmPerc: UILabel!
    @IBOutlet weak var sPerc: UILabel!
    
    @IBOutlet weak var ePerc: UILabel!
    @IBOutlet weak var cPerc: UILabel!
    
    @IBOutlet weak var message: UITextView!
    
    struct Stats: Codable{
        var overall:Int
        var rm:Int
        var pw:Int
        var nt:Int
        var sc:Int
        var dm:Int
        var s:Int
        var el:Int
        var c:Int 
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let gradientLayer = CAGradientLayer()
        gradientLayer.frame = view.bounds
        gradientLayer.colors = [#colorLiteral(red: 0.9686274529, green: 0.78039217, blue: 0.3450980484, alpha: 1).cgColor, #colorLiteral(red: 0.8549019694, green: 0.250980407, blue: 0.4784313738, alpha: 1).cgColor]
        gradientLayer.shouldRasterize = true
        mainView.layer.addSublayer(gradientLayer)
        
        var shouldAutorotate: Bool {
            return false
        }
        
        func trackProgressBar(x: Int, y: Int, radius: Int, lineWidth: Int,view: UIView) {
            let trackLayer = CAShapeLayer()
            let center = CGPoint(x:x, y:y)
            let fullcircularPath = UIBezierPath(arcCenter: center, radius: CGFloat(radius), startAngle: -CGFloat.pi/2, endAngle: 2*CGFloat.pi, clockwise: true)
            trackLayer.path = fullcircularPath.cgPath
            
                trackLayer.strokeColor = UIColor.black.cgColor
                trackLayer.lineWidth = CGFloat(lineWidth)
                trackLayer.fillColor = UIColor.clear.cgColor
                trackLayer.lineCap = CAShapeLayerLineCap.round
                view.layer.addSublayer(trackLayer)
        }
            
        func realProgressBar (x: Int, y:Int, radius: Int, p:Float, lineWidth: Int, view: UIView, perc: UILabel) {
            let shapeLayer = CAShapeLayer()
            
            let center = CGPoint(x:x, y:y)
                
            
            let circularPath = UIBezierPath(arcCenter: center, radius: CGFloat(radius), startAngle: -CGFloat.pi/2, endAngle: (2*CGFloat.pi*CGFloat(p))-CGFloat.pi/2, clockwise: true)
                
            shapeLayer.path = circularPath.cgPath
            shapeLayer.strokeColor = UIColor.white.cgColor
            shapeLayer.lineWidth = CGFloat(lineWidth)
            shapeLayer.fillColor = UIColor.clear.cgColor
            shapeLayer.lineCap = CAShapeLayerLineCap.round
            shapeLayer.strokeEnd = 0
            
            view.layer.addSublayer(shapeLayer)
            
            let basicAnimation = CABasicAnimation(keyPath: "strokeEnd")
            basicAnimation.toValue = 1
            basicAnimation.duration = 2
            basicAnimation.fillMode = CAMediaTimingFillMode.forwards
            basicAnimation.isRemovedOnCompletion = false
            
            shapeLayer.add(basicAnimation, forKey: "urSoBasic")
            
            let percent = Int(p*100)
            
            perc.text = String(percent)+"%"
            
        }
        
        let url = URL(string: "http://127.0.0.1:5000/quizstat")!
        
        let task = URLSession.shared.dataTask(with: url) {(data, response, error) in
            let jsonString = String(data: data!, encoding: .utf8)!
            print(jsonString)
            
            if let jsonData = jsonString.data(using: .utf8) {
                let decoder = JSONDecoder()
                
                do {
                    let stat = try decoder.decode(Stats.self, from: jsonData)
                    OperationQueue.main.addOperation {
                        trackProgressBar(x: 75, y: 75, radius: 65, lineWidth: 15, view: self.progressbar)
                        realProgressBar(x: 75, y: 75, radius: 65, p: Float(stat.overall)/100.0, lineWidth: 15, view: self.progressbar, perc: self.overallPerc)
                        
                        trackProgressBar(x: 40, y: 40, radius: 35, lineWidth: 10, view: self.rmprogressbar)
                        realProgressBar(x: 40, y: 40, radius: 35, p: Float(stat.rm)/100.0, lineWidth: 10, view: self.rmprogressbar, perc: self.rmPerc)
                        
                        trackProgressBar(x: 40, y: 40, radius: 35, lineWidth: 10, view: self.pwprogressbar)
                        realProgressBar(x: 40, y: 40, radius: 35, p: Float(stat.pw)/100.0, lineWidth: 10, view: self.pwprogressbar, perc: self.pwPerc)
                        
                        trackProgressBar(x: 40, y: 40, radius: 35, lineWidth: 10, view: self.ntprogressbar)
                        realProgressBar(x: 40, y: 40, radius: 35, p: Float(stat.nt)/100.0, lineWidth: 10, view: self.ntprogressbar, perc: self.ntPerc)
                        
                        trackProgressBar(x: 40, y: 40, radius: 35, lineWidth: 10, view: self.scprogressbar)
                        realProgressBar(x: 40, y: 40, radius: 35, p: Float(stat.sc)/100.0, lineWidth: 10, view: self.scprogressbar, perc: self.scPerc)
                        
                        trackProgressBar(x: 40, y: 40, radius: 35, lineWidth: 10, view: self.dmprogressbar)
                        realProgressBar(x: 40, y: 40, radius: 35, p: Float(stat.dm)/100.0, lineWidth: 10, view: self.dmprogressbar, perc: self.dmPerc)
                        
                        trackProgressBar(x: 40, y: 40, radius: 35, lineWidth: 10, view: self.sprogressbar)
                        realProgressBar(x: 40, y: 40, radius: 35, p: Float(stat.s)/100.0, lineWidth: 10, view: self.sprogressbar, perc: self.sPerc)
                        
                        trackProgressBar(x: 40, y: 40, radius: 35, lineWidth: 10, view: self.eprogressbar)
                        realProgressBar(x: 40, y: 40, radius: 35, p: Float(stat.el)/100.0, lineWidth: 10, view: self.eprogressbar, perc: self.ePerc)
                        
                        trackProgressBar(x: 40, y: 40, radius: 35, lineWidth: 10, view: self.cprogressbar)
                        realProgressBar(x: 40, y: 40, radius: 35, p: Float(stat.c)/100.0, lineWidth: 10, view: self.cprogressbar, perc: self.cPerc)
                        
                    }
                    
                } catch {
                    print(error.localizedDescription)
                }
                
            } else {
                print(error!)
            }
        }
        task.resume()
        
        let url2 = URL(string: "http://127.0.0.1:5000/statsmessage")!
        
        let task2 = URLSession.shared.dataTask(with: url2) {(data, response, error) in
            let jsonString = String(data: data!, encoding: .utf8)!
            OperationQueue.main.addOperation {
                self.message.text = jsonString
            }
        }
        task2.resume()
        
    }
}
