sim=require'sim'

function sysCall_init()
    visionSensorHandle=sim.getObject("../sensor")
    sensorBaseHandle=sim.getObject('..')

    maxScanDistance=10.0
    maxScanDistance_=maxScanDistance*0.9999

    pcall(function()
        sim.setObjectFloatParam(visionSensorHandle,sim.visionfloatparam_far_clipping,maxScanDistance)
    end)

    scanningAngle=45*math.pi/180
    pcall(function()
        sim.setObjectFloatParam(visionSensorHandle,sim.visionfloatparam_perspective_angle,scanningAngle)
    end)

    showPoints=true
    red={1,0,0}
    points=sim.addDrawingObject(sim.drawing_spherepts,0.01,0,-1,100000,nil,nil,nil,red)
end

function sysCall_cleanup()
end

function sysCall_sensing()
    measuredData={}
    
    if notFirstHere then
        sim.addDrawingObjectItem(points,nil)
        r,t1,u1=sim.readVisionSensor(visionSensorHandle)
    
        m1=sim.getObjectMatrix(visionSensorHandle)
        m01=sim.getObjectMatrix(sensorBaseHandle)
        m01=sim.getMatrixInverse(m01)
        m01=sim.multiplyMatrices(m01,m1)

        if u1 then
            for j=0,u1[2]-1,1 do
                for i=0,u1[1]-1,1 do
                    w=2+4*(j*u1[1]+i)
                    v1=u1[w+1]
                    v2=u1[w+2]
                    v3=u1[w+3]
                    v4=u1[w+4]
                    if (v4<maxScanDistance_) then
                        p={v1,v2,v3}
                        p=sim.multiplyVector(m01,p)
                        
                        -- Ambil semua titik di luar jarak 0.2m (bodi drone)
                        local dist = math.sqrt(p[1]^2 + p[2]^2 + p[3]^2)
                        if dist > 0.2 then
                            table.insert(measuredData,p[1])
                            table.insert(measuredData,p[2])
                            table.insert(measuredData,p[3])
                        end
                    end
                    if showPoints then
                        p={v1,v2,v3}
                        p=sim.multiplyVector(m1,p)
                        sim.addDrawingObjectItem(points,p)
                    end
                end
            end
        end
    end
    notFirstHere=true
    
    -- Kirimkan Sinyal Biner Pakai sim.packFloatTable
    if #measuredData > 0 then
        local packedData = sim.packFloatTable(measuredData)
        sim.setBufferSignal("fast3D_data", packedData)
    end
end