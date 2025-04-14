import cv2
import numpy as np
import matplotlib.pyplot as plt


def main():
    cap = cv2.VideoCapture(1) # захват видео с i-ой веб камеры
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('outputVIDEO.avi', fourcc, 20.0, (640, 480)) # запись видео

    roi_selected = False # проверяем обрезан ли кадр до нужного размера
    draw_line = False  # Флаг для отслеживания, нужно ли рисовать линию
    frame_count = 0

    print("*******Спектроскоп*******")
    print("l - показать линию на экране (по центру)")
    print("a - анализ спектра")
    print("r - выделить часть экрана")
    print("s - сохранить кадр")
    print("q - завершить видео")

    while (True):
        ret, frame = cap.read() # если кадр был считан верно, то возвращается True. (+ сам кадр)
        out.write(frame) # запись видео

        if draw_line:
            height, width, _ = frame.shape  # Получаем размеры кадра
            center_x = width // 2  # Вычисляем X координату центра

            # Рисуем вертикальную линию
            cv2.line(frame, (center_x, 0), (center_x, height), (0, 255, 0),
                     1)  # (0, 255, 0) - зеленый цвет, 1 - толщина линии

        k = cv2.waitKey(1)

        if k & 0xFF == ord('l'):
            draw_line = not draw_line

        if k & 0xFF == ord('s'):
            filename = input("Enter filename for saving image (e.g., name.png or name): ")
            if not filename:  # проверяем, что ввод не пустой
                frame_count += 1
                filename = f"saved_frame_{frame_count}.png"

            if '.' not in filename:  # Если расширение не указано, добавляем .png по умолчанию
                filename += ".png"

            cv2.imwrite(filename, frame)  # Сохраняем кадр
            print(f"Saved frame as: {filename}")

        if k & 0xFF == ord('a') and (roi_selected == True): # выплняется если ввели s и roi_selected == True

            shape = cropped.shape # присваем shape кортеж из ширины, высоты и кол-ва каналов обрезанного кадра

            r_dist = []
            b_dist = []
            g_dist = []
            all_dist = []
            for i in range(shape[1]): # итерируемся по всем столбцам кадра (по всей ширине)
                b_val = np.mean(cropped[:, i][:, 0]) # сщитаем среднюю интенсивность красного канала для i-го столбца
                g_val = np.mean(cropped[:, i][:, 1])
                r_val = np.mean(cropped[:, i][:, 2])
                all_val = (r_val + b_val + g_val)

                r_dist.append(r_val)
                g_dist.append(g_val)
                b_dist.append(b_val)
                all_dist.append(all_val)

            r_dist = np.array(r_dist)
            g_dist = np.array(g_dist)
            b_dist = np.array(b_dist)
            all_dist = np.array(all_dist)

            plt.figure().set_size_inches(10, 7)

            ax = plt.subplot(211)
            roi = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])] # обрезаем кадр
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB) # преобразовываем значения пикселей в область видимого спектра
            plt.title('Фото спектра')
            plt.imshow(roi) # выводим на экран готовый кадр

            plt.subplot(212, sharex=ax)
            max_value = np.max(all_dist)

            plt.plot(r_dist/max_value, color='r', label='red', alpha=0.5)
            plt.plot(g_dist/max_value, color='g', label='green', alpha=0.5)
            plt.plot(b_dist/max_value, color='b', label='blue', alpha=0.5)
            plt.plot(all_dist/max_value, color='black', label='all')

            plt.legend(loc="best")
            plt.title('Зависимость относительной интенсивности столбца кадра от номера столбца')
            plt.xlabel('n')
            plt.ylabel('$I/I_0$')
            plt.savefig('outputPHOTO.pdf')
            plt.show()

        elif k & 0xFF == ord('r'):
            r = cv2.selectROI(frame) # обрезаем нужную часть кадра
            roi_selected = True

        elif k & 0xFF == ord('q'): # заканчиваем работу
            break

        else:
            if roi_selected:
                cropped = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
                cv2.imshow('roi', cropped)
            else:
                cv2.imshow('frame', frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()